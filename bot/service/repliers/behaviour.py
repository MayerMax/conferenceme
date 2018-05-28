from bot.service.repliers.guest import GuestTelegramReplier
from bot.service.repliers.telegram_replier import TelegramReplier
from bot.service.users.user import User


class UserBehaviour:
    def __init__(self):
        """
        класс для обсулживания телеграм пользователей
        """
        self.authorized_users = set()  # множество гостевых пользователей
        self.guest_users = set()  # множество авторизованных
        self.repliers = {}
        self.authorized_where_to_search = {}

    def remove_authorized_user(self, user: User):
        if user in self.authorized_users:
            self.authorized_users.remove(user)
            return True
        return False

    def add_guest(self, user: User):
        self.guest_users.add(user)
        self.create_replier(user)

    def add_authorized(self, user: User, key: int):
        self.guest_users.remove(user)
        self.authorized_users.add(user)
        self.create_replier(user)
        self.authorized_where_to_search[user] = key

    def get_available_replier(self, user: User):
        return self.repliers.get(user, None)

    def create_replier(self, user: User):
        if user in self.authorized_users:
            self.repliers[user] = TelegramReplier()
            return
        if user in self.guest_users:
            self.repliers[user] = GuestTelegramReplier()
            return

    def is_authorized(self, user: User):
        return user in self.authorized_users

    def get_conference_id(self, user: User):
        return self.authorized_where_to_search.get(user)

