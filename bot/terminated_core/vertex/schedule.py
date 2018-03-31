from typing import Tuple, List

from bot.query import QueryResult
from bot.terminated_core.vertex.vertex import BaseActionVertex


class ScheduleWeekVertex(BaseActionVertex):
    def predict_is_suitable_input(self, user_raw_query) -> bool:
        pass

    def activation_function(self, user_raw_query, user_data, hierarchy, search_source) -> Tuple[QueryResult, List[str]]:
        pass


class ScheduleTodayVertex(BaseActionVertex):
    def predict_is_suitable_input(self, user_raw_query) -> bool:
        pass

    def activation_function(self, user_raw_query, user_data, hierarchy, search_source) -> Tuple[QueryResult, List[str]]:
        pass


class ScheduleTomorrowVertex(BaseActionVertex):
    def predict_is_suitable_input(self, user_raw_query) -> bool:
        pass

    def activation_function(self, user_raw_query, user_data, hierarchy, search_source) -> Tuple[QueryResult, List[str]]:
        pass


class ScheduleSectionVertex(BaseActionVertex):
    def predict_is_suitable_input(self, user_raw_query) -> bool:
        pass

    def activation_function(self, user_raw_query, user_data, hierarchy, search_source) -> Tuple[QueryResult, List[str]]:
        pass
