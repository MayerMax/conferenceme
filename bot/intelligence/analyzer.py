from bot.query import QueryResult, QueryRequest
from bot.service.history import Context
from bot.statuses import StatusTypes
from bot.terminated_core.graph.create import create_graph


class Analyzer:
    def __init__(self):
        """класс, отвечающий за работу над пользовательским запросом"""
        self.__graph = create_graph()
        self.user_context = {}

    def analyze(self, request: QueryRequest) -> QueryResult:
        asked_user = request.who_asked
        if asked_user.username not in self.user_context:
            self.user_context[asked_user.username] = Context(asked_user.username)

        user_context = self.user_context.get(asked_user.username)

        #     pass  # now no NLP analyzing
        request = self.__translate(request)
        return self.__analyze(request, user_context)

    def __analyze(self, request: QueryRequest, user_context: Context) -> QueryResult:
        last_action = user_context.peek()
        if not last_action:
            return self.__activate_vertex_and_record(request.question, request, user_context)

        last_vertex = self.__graph.get_action_vertex(last_action.vertex_name)
        print(last_vertex.get_children_alternative_names())

        if last_vertex.status == StatusTypes.LEAF:
            request.question = 'Exit state'
            return self.__activate_vertex_and_record('Welcome', request, user_context)

        most_probable = self.__graph.test_vertex_activation_against_input_and_return(last_action.vertex_name,
                                                                                     request, user_context, 0.7)
        if not most_probable:
            request.question = 'Do not understand'
            return self.__activate_vertex_and_record('Welcome', request, user_context)
            # нужно написать более развернутую ошибку

        return self.__activate_vertex_and_record(most_probable, request, user_context)

    def __translate(self, request: QueryRequest) -> QueryRequest:
        """
        Функция для NLP анализа в общем случае и для конвертирования альтернативных имен вершин графа в настоящием имена
        в частном случае
        :param request: запрос пользователя
        :return: поправленный QueryRequest так, чтобы он мог быть распознан графом
        """
        vertex = self.__graph.get_action_vertex_via_alternative_name(request.question)
        if vertex:
            request.question = vertex.name
            return request
        return request

    def __activate_vertex_and_record(self, vertex_name:str, request: QueryRequest, user_context: Context) -> QueryResult:
        query_result = self.__graph.activate_vertex(vertex_name, request, user_context)
        user_context.add_record(vertex_name, request.question, query_result)
        return query_result
