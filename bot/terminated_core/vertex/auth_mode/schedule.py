import dateparser
import datetime
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

by_all_results = {
    'Success': '{}, лови расписание:\n\n{}',
    'Empty': 'Ничего не нашлось, видимо конференция еще не готова организаторами'
}

by_today_results = {
    'Success': 'Супер, вот какие лекции еще будут:\n\n{}',
    'Empty': 'На сегодня уже ничего нет, либо же и вовсе не было'
}


def get_lectures_by_date(conf_id, date):
    a = Alchemy.get_session()
    return [x for x in a.query(Lecture).filter(Lecture.conf_id == conf_id).all() if x.when.day == date.day
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


class ScheduleAllVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        a = Alchemy.get_session()
        lectures = a.query(Lecture).filter(Lecture.conf_id == request.where_to_search).order_by(Lecture.when).all()

        if not lectures:
            answer = by_all_results.get('Empty')
        else:
            answer = '\n'.join('{} - {}'.format(x.topic, x.when) for x in lectures)
            answer = by_all_results.get('Success').format(request.who_asked.username, answer)
        return QueryResult(StatusTypes.LEAF, [answer],
                           [None], [])


class ScheduleTodayVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        today = datetime.datetime.now()
        conf_id = request.where_to_search
        lectures = get_lectures_by_date(conf_id, today)
        print(len(lectures))
        only_fresh = [x for x in lectures if x.when.hour >= today.hour]
        print(only_fresh)

        if only_fresh:
            answer = '\n'.join('{} - {}'.format(x.topic, x.when) for x in only_fresh)
            answer = by_today_results.get('Success').format(answer)
        else:
            answer = by_today_results.get('Empty')

        return QueryResult(StatusTypes.LEAF, [answer], [None], [])
