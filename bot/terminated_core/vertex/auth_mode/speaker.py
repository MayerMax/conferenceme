import emoji
import os
import textdistance

from bot.intelligence.photosim import ConferencePhotoModel
from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.statuses import StatusTypes, RequestType

from bot.terminated_core.vertex.vertex import BaseActionVertex
from db.alchemy import Alchemy
from db.models.people import Speaker

all_speakers_vertex = {
    'Success': 'Отлично! Вот список всех спикеров конференции!\n{}',
}

search_transitions = emoji.emojize('Супер, теперь напиши имя лектора (будет хорошо, если укажешь фамилию тоже).\n'
                                   'Кстати, можешь сфоткать его - и я попробую разобраться :camera:')

search_finish = {
    'Failure': 'WOW! Я никого не нашел! Думаю, ты ошибся, попробуй ввести еще раз!',
    'Continue': 'Вау, есть несколько подходящих вариантов, не понятно как выбрать. Укажи мне сам',
    'Success': 'Лови: {}',
    'PFailure': 'Вот это да, мне не удалось найти знакомых лиц на твоей фотке\nДавай попробуем еще раз?',
    'PSuccess': 'супер, я нашел!\n{}'
}

# CPM = ConferencePhotoModel(img_dir='/Users/smallhamster/Documents/conferenceme/db/media//speakers')


def find_image(speakers, photo_path):
    # found_face_path = CPM.find_relevant_face(photo_path)
    found_face_path = None
    if not found_face_path:
        return None
    found_face_path = os.path.normpath(found_face_path[0])
    return [speaker for speaker in speakers if speaker.photo_path == found_face_path][0]


class SpeakerVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, ['Отлично, что именно хочешь узнать'], [None],
                           self.get_children_alternative_names())


class AllSpeakersVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        all_speakers = Alchemy.get_session().query(Speaker).filter(Speaker.conf_id == request.where_to_search).all()
        speakers_representation = '\n'.join([str(x) for x in all_speakers])

        return QueryResult(StatusTypes.LEAF, [all_speakers_vertex.get('Success').format(speakers_representation)],
                           [None], [])


class SearchSpeakerTransitionVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, [search_transitions], [None], [],
                           )


class SearchSpeakerFinishVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        if request.request_type == RequestType.PHOTO:
            return True

        speakers = Alchemy.get_session().query(Speaker).filter(Speaker.conf_id == request.where_to_search).all()

        close_similar = [textdistance.jaccard.distance(request.question.lower(), speaker.name.lower()) for speaker in
                         speakers]
        max_sim = min(close_similar)
        request.edition = [speakers[idx].name for idx, value in enumerate(close_similar) if value <= 0.48]
        if max_sim < 0.2:
            request.question = speakers[close_similar.index(max_sim)].name
        elif len(request.edition) == 1:
            request.question = request.edition[0]
        else:
            request.need_more = True

        return True

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        if request.request_type == RequestType.STRING:
            return self.__process_string(request, context)
        if request.request_type == RequestType.PHOTO:
            return self.__process_image(request, context)

    def __process_string(self, request: QueryRequest, context: Context) -> QueryResult:
        if request.need_more:
            if len(request.edition) < 1:
                return QueryResult(StatusTypes.LEAF, [search_finish.get('Failure')], [None], [], False)

            if len(request.edition) > 1:
                return QueryResult(StatusTypes.LEAF, [search_finish.get('Continue')], [None], request.edition, False)

        else:
            speakers = Alchemy.get_session().query(Speaker).filter(Speaker.conf_id == request.where_to_search).all()
            speaker = [speaker for speaker in speakers if speaker.name == request.question][0]
            return QueryResult(StatusTypes.LEAF, [search_finish.get('Success').format(str(speaker))],
                               [speaker.photo_path], self.to_roots, True)

    def __process_image(self, request: QueryRequest, context: Context) -> QueryResult:
        photo_path = request.question
        # сделано плохо - только для одной конференции и все - КОСТЫЛЬ
        speakers = Alchemy.get_session().query(Speaker).filter(Speaker.conf_id == request.where_to_search).all()
        found = find_image(speakers, photo_path)
        if not found:
            return QueryResult(StatusTypes.LEAF, [search_finish.get('PFailure')], [None], [], False)
        return QueryResult(StatusTypes.LEAF, [search_finish.get('PSuccess').format(found)], [found.photo_path], [])
