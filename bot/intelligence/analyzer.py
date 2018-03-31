from bot.service.conference_plain_object import ConferencePlainObject
from bot.terminated_core.graph.create import create_graph
from bot.terminated_core.graph.state_graph import StateGraph


class Analyzer:
    def __init__(self):
        """класс, отвечающий за работу над пользовательским запросом"""
        self.__graph = create_graph()
        self.user_context = {}

    def analyze(self, user_raw_query: str, user_data: dict, search_source: ConferencePlainObject):
        pass
