import telegram

from db.alchemy import Alchemy


class Auth:
    """
    класс для хранения авторзованных ботом пользователей
    """

    def __init__(self, alchemy: Alchemy = None):
        if alchemy:
            self.alchemy = alchemy
        else:
            self.alchemy = Alchemy('../../db/data.db')
        self.__authorized_users = set()

    def register_user(self, user_nickname: str, string_password: str) -> bool:
        """
        функция регистрации пользователя
        :param user_nickname: имя пользователя в мессенджере
        :param string_password: пароль доступа к конференции
        :return: True - если удачно, False - иначе
        """
        if self.alchemy.is_correct_key(string_password):
            self.__authorized_users.add(user_nickname)
            return True
        return False

    def is_authorized(self, user_nickname: str) -> bool:
        """
        функция проверки пользователя на авторизацию
        :param user_nickname: имя пользователя в мессенджере
        :return: True или  False
        """
        return user_nickname in self.__authorized_users
