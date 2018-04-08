import emoji
import textdistance

from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.statuses import StatusTypes, RequestType
from bot.terminated_core.vertex.vertex import BaseActionVertex


class ContentVertex(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(
            status=StatusTypes.NEIGHBOUR,
            answer=['Отлично, с чем именно тебе помочь?'],
            attachments=[None],
            extra_args=self.get_children_alternative_names(),
        )

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name


class BeginAskAboutSpeaker(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(
            status=StatusTypes.NEIGHBOUR,
            answer=[emoji.emojize('Супер, теперь напиши имя лектора (будет хорошо, если укажешь фамилию тоже).\n'
                                  'Кстати, можешь сфоткать его - и я попробую разобраться :camera:')],
            attachments=[None],
            extra_args=[],
        )

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name


class AskAboutSpeaker(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        # TODO индексация данных для ускорения
        if request.request_type == RequestType.STRING:
            return self.__process_string(request, context)
        else:
            return self.__process_image(request, context)

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        # TODO индексация данных для ускорения
        if request.request_type == RequestType.AUDIO:
            return False

        if request.request_type == RequestType.PHOTO:
            return True
        speakers = request.where_to_search.get_speakers()
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

    def __process_string(self, request: QueryRequest, context: Context) -> QueryResult:
        if request.need_more:
            if len(request.edition) < 1:
                return QueryResult(
                    status=StatusTypes.LEAF,
                    answer=['WOW! Я никого не нашел! Думаю, ты ошибся, попробуй ввести еще раз!'],
                    attachments=[None],
                    extra_args=[],
                    is_completed=False
                )
            if len(request.edition) > 1:
                return QueryResult(
                    status=StatusTypes.LEAF,
                    answer=['Вау, есть несколько подходящих вариантов, не понятно как выбрать. Укажи мне сам'],
                    attachments=[None],
                    extra_args=request.edition,
                    is_completed=False
                )

        else:
            speakers = request.where_to_search.get_speakers()
            speaker = [speaker for speaker in speakers if speaker.name == request.question][0]
            return QueryResult(
                status=StatusTypes.LEAF,
                answer=['Лови: {}'.format(str(speaker))],
                attachments=[speaker.photo_path],  # отправить снимок
                extra_args=self.to_roots,
                is_completed=True
            )

    def __process_image(self, request: QueryRequest, context: Context) -> QueryResult:
        pass
