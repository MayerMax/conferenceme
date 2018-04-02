from collections import namedtuple

User = namedtuple('User', ['id', 'first_name', 'last_name', 'username', 'language_code'])


class MakeUser:
    def __init__(self):
        pass

    @classmethod
    def from_telegram(cls, telegram_user) -> User:
        """
        Парсет объект телеграм пользователя в общий объект User
        :param telegram_user: объект телеграм пользователя
        :return:  User
        """
        pass
