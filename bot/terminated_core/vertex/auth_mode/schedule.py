import dateparser
from sqlalchemy import and_

from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.statuses import StatusTypes
from bot.terminated_core.vertex.vertex import BaseActionVertex
from db.alchemy import Alchemy
from db.models.content import Lecture

by_date_results = {
    'Success': 'Отлично, нашел следующие лекции: {}',
    'Empty': 'В указанный тобой день ничего нет',
    'Failure': 'Не смог распознать дату, извини'
}


def get_lectures_by_date(conf_id, date):
    a = Alchemy.get_session()
    return [x for x in a.query(Lecture).filter(and_(Lecture.conf_id == conf_id)).all() if x.when.date == date.day
            and x.when.year == date.year and x.when.month == date.month]


class ScheduleVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, ['Выберите опцию'], [None], self.get_children_alternative_names())


class ScheduleByDateTransitionVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, ['Отлично, напиши дату'], [None], [])


class ScheduleByDateFinishVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        parsed_result = dateparser.parse(request.question)
        if parsed_result:
            request.edition = parsed_result
            return True
        return False

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        date = request.edition
        conf_id = request.where_to_search
        lectures = get_lectures_by_date(conf_id, date)
        if lectures:
            answer = by_date_results.get('Success').format('\n'.join(str(x) for x in lectures))
        else:
            answer = by_date_results.get('Empty')
        return QueryResult(StatusTypes.LEAF, [answer], [None], [])