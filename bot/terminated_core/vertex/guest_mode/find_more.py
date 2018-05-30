import datetime

import textdistance

from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.statuses import StatusTypes, RequestType
from bot.terminated_core.vertex.vertex import BaseActionVertex
from db.alchemy import Alchemy
from db.models.event import Conference


class FindMoreAboutConferenceVertex(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, ['Выбери одно из следующих действий'], [None],
                           self.get_children_alternative_names())

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name


new_conference_response = {
    'Success': 'Супер, я нашел {} новых конференций(ии):\n',
    'Empty': 'Пока нет новых доступных конференций'
}

search_conference_finish = {
    'Success': '',
    'Failure': '',
    'Continue': 'Вау, есть несколько подходящих вариантов, не понятно как выбрать. Укажи мне сам'
}


class NewConferencesVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        today = datetime.datetime.now()
        a = Alchemy.get_session()
        fresh_conferences = [str(x) for x in a.query(Conference).filter(Conference.begin_date >= today).all()]
        answer = []
        if fresh_conferences:
            answer.append(new_conference_response.get('Success').format(len(fresh_conferences)))
            answer.extend(x for x in fresh_conferences)
        else:
            answer.append(new_conference_response.get('Empty'))

        return QueryResult(StatusTypes.LEAF, answer, [None] * len(answer), [])


class SearchConferenceByNameVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, ['Отлично, введи название интересующей тебя конференции'], [None], [])


class SearchConferenceByNameFinishVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        if request.request_type != RequestType.STRING:
            return False
        a = Alchemy.get_session()
        conferences = {c.name: c for c in a.query(Conference).all()}
        similarity_to_conference = {
        textdistance.jaccard.distance(request.question.lower(), conference.lower()): conference
        for conference in conferences}

        max_sim = min(similarity_to_conference)
        request.edition = [similarity_to_conference[value] for value in similarity_to_conference if value <= 0.48]
        if max_sim < 0.2:
            request.question = str(conferences[similarity_to_conference[max_sim]])
        elif len(request.edition) == 1:
            request.question = str(conferences[request.edition[0]])
        else:
            request.need_more = True
            request.question = list(conferences)
        return True

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        if request.need_more:
            if len(request.edition) < 1:
                return QueryResult(StatusTypes.LEAF, ['Мне не удалось ничего найти'], [None], [])

            if len(request.edition) > 1:
                return QueryResult(StatusTypes.LEAF, [search_conference_finish.get('Continue')], [None],
                                   request.edition, is_completed=False)
        answer = ['Лови:\n{}'.format(request.question),
                  'Если хочешь пройти регистрацию - перейди по ссылке:\nhttps://www.sberbank.ru/']

        return QueryResult(StatusTypes.LEAF, answer, [None]*len(answer), [])
