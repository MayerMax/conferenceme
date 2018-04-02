from bot.query import QueryResult
from bot.service.conference_plain_object import ConferencePlainObject
from bot.service.history import Context
from bot.terminated_core.graph.create import create_graph


class Analyzer:
    def __init__(self):
        """класс, отвечающий за работу над пользовательским запросом"""
        self.__graph = create_graph()
        self.user_context = {}

    def analyze(self, user_raw_query: str, user_data, search_source: ConferencePlainObject) -> QueryResult:
        if user_data.username not in self.user_context:
            self.user_context[user_data.username] = Context(user_data.username)
        user_context = self.user_context.get(user_data.username)
        if not user_context.peek():
            return self._begin_analyzer(user_raw_query, user_data, search_source, user_context)
        return self._transition_state_analyzer(user_raw_query, user_data, search_source, user_context)

    def _begin_analyzer(self, user_raw_query: str, user_data, search_source: ConferencePlainObject,
                        user_context: Context) -> QueryResult:
        query_result = self.__graph.activate_vertex('Welcome', [user_raw_query, user_data,
                                                                user_context, search_source])
        user_context.add_record('Welcome', user_raw_query, query_result)
        return query_result

    def _transition_state_analyzer(self, user_raw_query: str, user_data, search_source: ConferencePlainObject,
                                   user_context: Context) -> QueryResult:
        previous_vertex = self.__graph.get_action_vertex(user_context.peek().vertex_name)
        if user_raw_query in previous_vertex.get_children_names():
            pass # Test input against predictions
        return None # Todo
