import datetime

import dateparser
import textdistance

import emoji

from bot.query import QueryResult, QueryRequest
from bot.service.history import Context
from bot.statuses import StatusTypes
from bot.terminated_core.vertex.vertex import BaseActionVertex


class ScheduleSectionVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return True if request.question == self.alternative_name or request.question == self.name else False

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, ['класс, теперь уточним секцию'], [None], [])


class ScheduleAskVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        """
        Сравнивает запрос с известными секциями, и если сравнение удалось - правит пользовательский запрос, занося
        изменение в поле edition
        :param request: пользовательский запрос
        :param context: история
        :return: True или False
        """
        question = request.question.lower()
        cpo = request.where_to_search
        find_closes = [textdistance.jaccard.distance(question, section.name.lower())
                       for section in cpo.get_sections()]
        max_close = min(find_closes)
        if max_close > 0.6:
            return False

        correct_section = cpo.get_sections()[find_closes.index(max_close)]
        request.edition = correct_section.name
        return True

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        if request.edition is not None:
            inserted = request.edition
        else:
            inserted = request.question
        return QueryResult(StatusTypes.NEIGHBOUR,
                           [emoji.emojize('Отлично, я нашел секцию "{}" :thumbs_up:.\n'
                                          'Еще несколько уточнений. На какое время нужно расписание?'.format(
                               inserted))], [None],
                           self.get_children_alternative_names())


class ScheduleDateAskVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, [emoji.emojize('Так, понял, на какое число тебе дать расписание?\n'
                                                                 'Будет лучше, если введешь что-то в '
                                                                 'таком формате: день-меся-год :clock2:')], [None], [])


class ScheduleByDateVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        parsed_result = dateparser.parse(request.question)
        if parsed_result:
            request.edition = parsed_result
            return True
        return False

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        date = request.edition
        cpo = request.where_to_search
        parent_node = context.peek().previous
        if parent_node.vertex_name != self.parent.parent.name:
            print('ALERT')

        section = parent_node.request
        satisfy_condition = cpo.get_section_schedule(date, section)
        if not satisfy_condition:
            return QueryResult(StatusTypes.LEAF, [emoji.emojize('{}, прости, на этот день ничего не смог найти '
                                                                ':tired_face:'.format(
                request.who_asked.first_name))],
                               [None], self.to_roots)
        else:
            return QueryResult(StatusTypes.LEAF, ['{}, отлично! :stuck_out_tongue:\n Держи расписание '
                                                  'и короткое описание\n {}'.format(request.who_asked.first_name,
                                                                                    '\n'.join(
                                                                                        str(x) for x in
                                                                                        satisfy_condition))],
                               [None], self.to_roots)


class ScheduleTodayVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return self.name == request.question or self.alternative_name == request.question

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        cpo = request.where_to_search
        parent_node = context.peek()
        if parent_node.vertex_name != self.parent.name:
            print('ALERT')

        section = parent_node.request
        today = datetime.datetime.now()
        satisfy_condition = cpo.get_section_schedule(today, section)
        if not satisfy_condition:
            return QueryResult(StatusTypes.LEAF, [emoji.emojize('{}, прости, на этот день ничего не смог найти '
                                                                ':tired_face:'.format(
                request.who_asked.first_name))],
                               [None], self.to_roots)
        else:
            return QueryResult(StatusTypes.LEAF, ['{}, отлично! :stuck_out_tongue:\n Держи расписание '
                                                  'и короткое описание\n {}'.format(request.who_asked.first_name,
                                                                                    '\n'.join(
                                                                                        str(x) for x in
                                                                                        satisfy_condition))],
                               [None], self.to_roots)


class ScheduleTomorrowVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return self.name == request.question or self.alternative_name == request.question

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        cpo = request.where_to_search
        parent_node = context.peek()
        if parent_node.vertex_name != self.parent.name:
            print('ALERT')

        section = parent_node.request
        today = datetime.datetime.now() + datetime.timedelta(days=1)
        satisfy_condition = cpo.get_section_schedule(today, section)
        if not satisfy_condition:
            return QueryResult(StatusTypes.LEAF, [emoji.emojize('{}, прости, на этот день ничего не смог найти '
                                                                ':tired_face:'.format(
                request.who_asked.first_name))],
                               [None], self.to_roots)
        else:
            return QueryResult(StatusTypes.LEAF, ['{}, отлично! :stuck_out_tongue:\n Держи расписание '
                                                  'и короткое описание\n {}'.format(request.who_asked.first_name,
                                                                                    '\n'.join(
                                                                                        str(x) for x in
                                                                                        satisfy_condition))],
                               [None], self.to_roots)
