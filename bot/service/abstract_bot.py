import abc

from bot.intelligence.analyzer import Analyzer
from bot.service.auth import Auth
from bot.service.event_manager import EventManager
from bot.service.repliers.abstract_replier import AbstractReplier


class AbstractBot(metaclass=abc.ABCMeta):
    def __init__(self, em: EventManager = None, auth: Auth = None, replier: type = None):
        self.event_manager = em
        self.auth = auth
        self.analyzer = Analyzer()
        self.replier = replier
        self.user_repliers = {}  # replier-ы для пользователей

    def is_authorized(self, user_nickname: str):
        return self.auth.is_authorized(user_nickname)

    def complete_register(self, user_nickname:str, string_password:str):
        return self.auth.register_user(user_nickname, string_password)