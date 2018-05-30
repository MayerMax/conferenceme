import abc

from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.service.users.user import User


class Basic(metaclass=abc.ABCMeta):
    def __init__(self):
        self.user_context = {}

    @abc.abstractmethod
    def default_behaviour(self, request: QueryRequest) -> QueryResult:
        pass

    @abc.abstractmethod
    def analyze(self, request: QueryRequest) -> QueryResult:
        pass
