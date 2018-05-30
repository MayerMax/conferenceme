from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.statuses import StatusTypes
from bot.terminated_core.vertex.vertex import BaseActionVertex

result_string = 'Мы - команда ConferenceMe. Наши разработчики это: Максим, Елена, Даниил и Денис. ' \
                'Наш бот позволяет Вам проводить время на конференциях эффективно: ' \
                'искать спикеров, смотреть расписание и находить интересные контакты. ' \
                'Подробнее можешь почитать на нашем сайте http://rusvectores.org/ru/models/'


class AboutUsVertex(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.LEAF, [result_string], [None], [])

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name
