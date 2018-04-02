from collections import namedtuple

import telegram

User = namedtuple('User', ['id', 'first_name', 'last_name', 'username', 'language_code'])


class MakeUser:
    def __init__(self):
        pass

    @classmethod
    def from_telegram(cls, telegram_user:telegram.user.User) -> User:
        """
        Парсет объект телеграм пользователя в общий объект User
        :param telegram_user: объект телеграм пользователя
        :return:  User
        """
        return User(telegram_user.id, telegram_user.first_name, telegram_user.last_name, telegram_user.username,
                    telegram_user.language_code)
