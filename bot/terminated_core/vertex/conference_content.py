from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.terminated_core.vertex.vertex import BaseActionVertex


class ContentVertex(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        pass

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        pass
