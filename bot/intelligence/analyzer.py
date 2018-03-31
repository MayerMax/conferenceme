from bot.service.conference_plain_object import ConferencePlainObject
from bot.service.history import Context
from bot.terminated_core.graph.create import create_graph
from bot.terminated_core.graph.state_graph import StateGraph


class Analyzer:
    def __init__(self):
        """класс, отвечающий за работу над пользовательским запросом"""
        self.__graph = create_graph()
        self.user_context = {}

    def analyze(self, user_raw_query: str, user_data, search_source: ConferencePlainObject):
        if user_data.username not in self.user_context:
            self.user_context[user_data.username] = Context(user_data.username)
        user_context = self.user_context.get(user_data.username)
        
