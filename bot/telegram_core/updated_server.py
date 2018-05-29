import logging

import datetime
import random
import string

from bot.intelligence.analyzer import Analyzer
from bot.query import QueryRequest
from bot.service.repliers.behaviour import UserBehaviour
from bot.service.users.user import MakeUser
from bot.statuses import RequestType
from bot.telegram_core.keys import KEY

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from bot.terminated_core.graph.create import create_auth
from bot.terminated_core.graph.guest_create import create_guest
from db.alchemy import Alchemy

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=KEY)

dispatcher = updater.dispatcher

CPM = None


class Bot:
    def __init__(self):
        self.user_behaviour = UserBehaviour()
        self.analyzer = Analyzer(create_auth, 'Welcome')
        self.guest = Analyzer(create_guest, 'Welcome')

    def start_state(self, bot, update):
        current_user = MakeUser.from_telegram(update.message.from_user)  # создаем текущего пользователя

        # если пользователь пишет /start, то автоматически считаем, что он новый и его нужно обработать, не важно
        # был он авторизован или нет
        self.user_behaviour.remove_authorized_user(current_user)

        # очищаем контекст, если он был, для данного пользователя, чтобы не хранить лишнюю информацию
        self.analyzer.clean_user_context(current_user)
        self.guest.clean_user_context(current_user)

        # далее формируем искусственный запрос с приветствием для гостевого анализатора
        hello_guest_query = QueryRequest(current_user, 'Welcome', RequestType.STRING)
        # отправляем его анализатору и получаем ответ в виде упорядоченного набора действий
        query_result = self.guest.analyze(hello_guest_query)

        # создаем пользователю replier-a
        self.user_behaviour.add_guest(current_user)
        user_replier = self.user_behaviour.get_available_replier(current_user)
        user_replier.create_reply(query_result, [bot, update])

    def text_handler(self, bot, update):
        current_user = MakeUser.from_telegram(update.message.from_user)

        # поведение авторизованного пользователя
        if self.user_behaviour.is_authorized(current_user):
            user_request = QueryRequest(current_user, update.message.text, RequestType.STRING,
                                        self.user_behaviour.authorized_where_to_search[current_user])
            query_result = self.analyzer.analyze(user_request)
            self.user_behaviour.get_available_replier(current_user).create_reply(query_result, [bot, update])
            return

        # поведение для гостя
        else:
            user_request = QueryRequest(current_user, update.message.text, RequestType.STRING)
            query_result = self.guest.analyze(user_request)
            # возможно, пользователь авторизовался
            if query_result.answer and query_result.answer[0] == 'AUTH OK':
                # теперь нужно добавить пользователя
                self.user_behaviour.add_authorized(current_user, query_result.answer[1])
                # теперь перенаправить к авторизованному анализатору
                hello_auth_query = QueryRequest(current_user, 'Welcome', RequestType.STRING)
                query_result = self.analyzer.analyze(hello_auth_query)
                self.user_behaviour.get_available_replier(current_user).create_reply(query_result, [bot, update])
                return
            else:
                # просто ответ для гостя
                self.user_behaviour.get_available_replier(current_user).create_reply(query_result, [bot, update])
                return

    def image_handler(self, bot, update):
        current_user = MakeUser.from_telegram(update.message.from_user)
        if self.user_behaviour.is_authorized(current_user):
            random_name = ''.join(random.choice(string.ascii_letters) for _ in range(16))
            path = update.message.photo[1].get_file().download(custom_path='../../db/media/temp/{}.jpg'.format(random_name))
            user_request = QueryRequest(current_user, path, RequestType.PHOTO,
                                        self.user_behaviour.authorized_where_to_search[current_user])

            analyzer_reply = self.analyzer.analyze(user_request)
            self.user_behaviour.get_available_replier(current_user).create_reply(analyzer_reply, [bot, update])
        else:
            fake_query = QueryRequest(current_user, 'FAKE')
            fake_answer = self.guest.analyze(fake_query)
            self.user_behaviour.get_available_replier(current_user).create_reply(fake_answer, [bot, update])

    def launch(self):
        start_handler = CommandHandler('start', self.start_state)
        text_handler = MessageHandler(Filters.text, self.text_handler)
        image_handler = MessageHandler(Filters.photo, self.image_handler)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(text_handler)
        dispatcher.add_handler(CallbackQueryHandler(self.button_callback))
        dispatcher.add_handler(image_handler)

        updater.start_polling()

    def button_callback(self, bot, update):
        query = update.callback_query
        if query.data == 'NONE':
            return
        user = MakeUser.from_telegram(query.from_user)

        qr = QueryRequest(user, query.data, RequestType.STRING)
        if self.user_behaviour.is_authorized(user):
            qr.where_to_search = self.user_behaviour.authorized_where_to_search[user]
            query_result = self.analyzer.analyze(qr)
        else:
            query_result = self.guest.analyze(qr)

        self.user_behaviour.get_available_replier(user).create_reply(query_result, [bot, query])
        return


if __name__ == '__main__':
    _ = Alchemy.get_instance('../../db/data.db')
    b = Bot()
    b.launch()
    print('GO')