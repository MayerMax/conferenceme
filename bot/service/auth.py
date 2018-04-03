from bot.service.users.user import User
from db.alchemy import Alchemy
from db.api import ConferenceApi


class NoSuchAuthUser(Exception):
    pass


class Auth:
    """
    класс для хранения авторзованных ботом пользователей
    """

    def __init__(self):
        self.__known_users = set()
        self.__users = {}
        self.__users_pass = {}

    def register_user(self, user: User, string_password: str) -> bool:
        """
        функция регистрации пользователя
        :param user: объект пользователя
        :param string_password: пароль доступа к конференции
        :return: True - если удачно, False - иначе
        """
        self.__known_users.add(user.username)
        conf = ConferenceApi.is_correct_key(string_password)
        if conf:
            self.__users[user.username] = user
            self.__users_pass[user.username] = conf.conf_id
            return True
        return False

    def is_authorized(self, user_nickname: str) -> bool:
        """
        функция проверки пользователя на авторизацию
        :param user_nickname: имя пользователя в мессенджере
        :return: True или  False
        """
        return user_nickname in self.__users

    def get_user(self, user_nickname: str) -> User:
        """
        возвращает пользователя по его никнейму
        :param user_nickname: строка
        :return: User
        """
        if user_nickname not in self.__users:
            raise NoSuchAuthUser('The user {} is not authorized'.format(user_nickname))
        return self.__users[user_nickname]

    def get_user_conference(self, user_nickname:str) -> int:
        """
        возвращает id конференции, к которой у пользователя есть доступ
        :param user_nickname: строка
        :return: int
        """
        if user_nickname not in self.__users:
            raise NoSuchAuthUser('The user {} is not authorized'.format(user_nickname))
        return self.__users_pass[user_nickname]