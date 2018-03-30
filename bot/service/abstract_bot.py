import abc

from bot.intelligence.analyzer import Analyzer
from bot.service.auth import Auth
from bot.service.event_manager import EventManager
from bot.service.repliers.abstract_replier import AbstractReplier


class AbstractBot(metaclass=abc.ABCMeta):
    def __init__(self, em: EventManager = None, auth: Auth = None, replier: AbstractReplier = None):
        self.__event_manager = em
        self.__auth = auth
        self.__analyzer = Analyzer()
        self.__replier = replier
