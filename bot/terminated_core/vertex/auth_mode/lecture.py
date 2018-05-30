import textdistance as textdistance

from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.statuses import StatusTypes, RequestType
from bot.terminated_core.vertex.vertex import BaseActionVertex
from db.alchemy import Alchemy
from db.models.content import Lecture


lecture_results = {
    'Success': 'Вот что удалось найти:',
    'Empty': 'Ничего не удалось найти'
}


class LectureVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, ['Выберите опцию'], [None], self.get_children_alternative_names())


class LectureDisplayAllVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        a = Alchemy.get_session()
        lectures = [str(x) for x in a.query(Lecture).filter(Lecture.conf_id == request.where_to_search).all()]
        if lectures:
            answers = [lecture_results['Success']]
            answers.extend(str(x) for x in lectures)
        else:
            answers = [lecture_results['Empty']]
        return QueryResult(StatusTypes.LEAF, answers, [None] * len(answers), [])


class LectureByNameTransitionVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context):
        return request.question == self.name or request.question == self.alternative_name

    def activation_function(self, request: QueryRequest, context: Context):
        return QueryResult(StatusTypes.NEIGHBOUR, ['Введите название лекции'], [None], [])


class LectureByNameFinishVertex(BaseActionVertex):
    def predict_is_suitable_input(self, request: QueryRequest, context: Context):
        if request.request_type != RequestType.STRING:
            return False
        a = Alchemy.get_session()
        lectures = {l.topic: l for l in a.query(Lecture).filter(Lecture.conf_id == request.where_to_search).all()}
        similarity_to_lecture = {textdistance.jaccard.distance(request.question.lower(), lecture.lower()): lecture
                                 for lecture in lectures}
        max_sim = min(similarity_to_lecture)
        request.edition = [similarity_to_lecture[value] for value in similarity_to_lecture if value <= 0.48]
        if max_sim < 0.2:
            request.question = lectures[similarity_to_lecture[max_sim]].get_description()
        elif len(request.edition) == 1:
            request.question = lectures[request.edition[0]].get_description()
        else:
            request.need_more = True
            request.question = list(lectures)
        return True

    def activation_function(self, request: QueryRequest, context: Context):
        return self.__process_string(request, context)

    def __process_string(self, request: QueryRequest, context: Context) -> QueryResult:
        if request.need_more:
            if len(request.edition) < 1:
                return QueryResult(
                    status=StatusTypes.LEAF,
                    answer=['{}\n{}\n{}'.format('WOW! Я никого не нашел! Думаю, ты ошибся, попробуй ввести еще раз!',
                                                'Вот все доступные лекции:',
                                                '\n'.join(request.question))],
                    attachments=[None],
                    extra_args=[],
                    is_completed=True
                )
            if len(request.edition) > 1:
                return QueryResult(
                    status=StatusTypes.LEAF,
                    answer=['Вау, есть несколько подходящих вариантов, не понятно как выбрать. Укажи мне сам'],
                    attachments=[None],
                    extra_args=request.edition,
                    is_completed=False
                )
        return QueryResult(
                status=StatusTypes.LEAF,
                answer=['Лови:\n{}'.format(request.question)],
                attachments=[None],
                is_completed=True
            )
