import abc
from typing import List

from bot.query import QueryResult
from bot.statuses import UserState


class AbstractReplier(metaclass=abc.ABCMeta):
    def __init__(self, root_state_names: List[str]=None, default_state_names: List[str] = None,
                 state: UserState = UserState.GUEST):
        """
        конструктор абстрактного replier-a
        :param root_state_names: именя вершин со статусом ROOT
        :param default_state_names: имена вершин, которые доступные всегда, независимо от состояний
        """
        self.root_state_names = root_state_names
        self.default_state_names = default_state_names
        self.user_state = state

        self.stack = []


    def set_user_state(self, new_state: UserState):
        self.user_state = UserState

    @abc.abstractmethod
    def create_reply(self, query_result: QueryResult, extra_args: List[object]) -> object:
        """
        абстрактная функция, реализующая поведение replier-а.
        Каждый мессенджер должен реализовывать ее, чтобы подготовить ответ, который может быть отправлен ботом
        :param query_result: результат, который подготовил анализатор, и который должен быть представлен replier-ом
        :param extra_args: дополнительные параметры, которые могут быть переданы в каждый мессенджер
        :return: объект произвольного типа, который может быть отправлен ботом пользователю
        """
        pass
