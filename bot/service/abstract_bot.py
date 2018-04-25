import abc

from bot.intelligence.analyzer import Analyzer
from bot.service.auth import Auth
from bot.service.conference_plain_object import ConferencePlainObject
from bot.service.event_manager import EventManager
from bot.service.repliers.abstract_replier import AbstractReplier
from bot.service.users.user import User


class AbstractBot(metaclass=abc.ABCMeta):
    def __init__(self, em: EventManager = None, auth: Auth = None, replier: type = None):
        self.event_manager = em
        self.auth = auth
        self.analyzer = Analyzer()
        self.replier = replier
        self.user_repliers = {}  # replier-ы для пользователей
        self.auth_requested = set()

    def is_authorized(self, user_nickname: str):
        return self.auth.is_authorized(user_nickname)

    def complete_register(self, user:User, string_password:str):
        return self.auth.register_user(user, string_password)

    def get_conference_by_user_name(self, user_name:str) -> ConferencePlainObject:
        conf_id = self.auth.get_user_conference(user_name)
        return self.event_manager.get_conference(conf_id)