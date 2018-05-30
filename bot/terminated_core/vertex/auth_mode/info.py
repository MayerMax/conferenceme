from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.statuses import StatusTypes
from bot.terminated_core.vertex.vertex import BaseActionVertex
from db.alchemy import Alchemy
from db.models.event import Conference


class ConferenceInfoVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        a = Alchemy.get_session()
        conference = a.query(Conference).filter(Conference.id == request.where_to_search).one_or_none()
        answer = ['Здесь будет публиковаться информация о конференции, но сейчас просто приветствие', str(conference)]
        return QueryResult(StatusTypes.LEAF, answer, [None]*len(answer), [])