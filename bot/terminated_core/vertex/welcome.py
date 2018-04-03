from bot.query import QueryResult, QueryRequest
from bot.service.history import Context
from bot.statuses import StatusTypes
from bot.terminated_core.vertex.vertex import BaseActionVertex


class WelcomeVertex(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        if not context.peek():
            return QueryResult(StatusTypes.ROOT, [request.where_to_search.get_conference_summary()], [None],
                               self.get_children_names())  # Send attachment
        if request.question != self.name:
            QueryResult(StatusTypes.ROOT, ['хмм, что-то пошло не так!'], [None], self.get_children_names())
        return QueryResult(StatusTypes.ROOT, ['приветствую еще раз!'], [None], self.get_children_names())

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> float:
        return 1.0
