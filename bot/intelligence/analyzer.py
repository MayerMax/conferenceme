from bot.intelligence.basic import Basic
from bot.query import QueryResult, QueryRequest
from bot.service.history import Context
from bot.service.users.user import User
from bot.statuses import StatusTypes


class Analyzer(Basic):
    def __init__(self, create_graph_func, source_vertex_name:str):
        """класс, отвечающий за работу над пользовательским запросом"""
        Basic.__init__(self)
        self.__graph = create_graph_func()
        self.source_vertex_name = source_vertex_name

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

        if last_vertex.status == StatusTypes.LEAF and last_action.query_result.is_completed:
            return self.__activate_vertex_and_record(request.question, request, user_context)

        if last_vertex.status == StatusTypes.LEAF and not last_action.query_result.is_completed:
            last_vertex.predict_is_suitable_input(request, user_context)
            query_result = self.__graph.activate_vertex(last_vertex.name, request, user_context)
            if query_result.is_completed:
                user_context.add_record(last_vertex.name, request.question, query_result)
            return query_result


        most_probable = self.__graph.predict_vertex_activation_against_input_and_return(last_action.vertex_name,
                                                                                        request, user_context)

        if not most_probable:
            request.question = 'Do not understand'
            return self.__activate_vertex_and_record(self.source_vertex_name, request, user_context)
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

    def __activate_vertex_and_record(self, vertex_name: str, request: QueryRequest,
                                     user_context: Context) -> QueryResult:
        if vertex_name not in self.__graph.get_vertices_names():
            return QueryResult(
                status=StatusTypes.LEAF,
                answer=['Хмм, не понял, что такое {}'.format(request.question)],
                attachments=[None],
                extra_args=[],
            )

        query_result = self.__graph.activate_vertex(vertex_name, request, user_context)
        user_context.add_record(vertex_name, request.edition, query_result)

        return query_result

    def default_behaviour(self, request: QueryRequest) -> QueryResult:
        pass

    def clean_user_context(self, user: User):
        if user.username in self.user_context:
            self.user_context.pop(user.username)