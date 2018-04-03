from bot.query import QueryResult, QueryRequest
from bot.service.history import Context
from bot.statuses import StatusTypes
from bot.terminated_core.vertex.vertex import BaseActionVertex


class ScheduleSectionVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> float:
        return 1.0

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, ['класс, теперь уточним секцию'], [None], [])


class ScheduleAskVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> float:
        question = request.question
        cpo = request.where_to_search
        sections = [section.name for section in cpo.get_sections()]
        if question in sections:
            return 1
        return 0  # сравнение через ошибки

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, ['инфа об этой секции'], [None], self.get_children_names())


class ScheduleByDateVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> float:
        pass

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        pass


class ScheduleTodayVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> float:
        pass

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        pass


class ScheduleTomorrowVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> float:
        pass

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        pass
