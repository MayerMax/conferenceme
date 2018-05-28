from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.terminated_core.vertex.vertex import BaseActionVertex


class NewsVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        pass