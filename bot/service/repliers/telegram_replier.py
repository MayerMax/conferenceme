from bot.query import QueryResult
from bot.service.repliers.abstract_replier import AbstractReplier


class TelegramReplier(AbstractReplier):
    def create_reply(self, query_result: QueryResult) -> object:
        pass

