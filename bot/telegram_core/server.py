import logging

from bot.query import QueryRequest
from bot.service.abstract_bot import AbstractBot
from bot.service.auth import Auth
from bot.service.event_manager import EventManager
from bot.service.repliers.telegram_replier import TelegramReplier
from bot.service.users.user import User, MakeUser
from bot.statuses import UserState
from bot.telegram_core.keys import KEY

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from db.alchemy import Alchemy

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=KEY)
dispatcher = updater.dispatcher


class Bot(AbstractBot):
    def start_state(self, bot, update):
        current_user = MakeUser.from_telegram(update.message.from_user)
        if current_user.username not in self.user_repliers:
            self.user_repliers[current_user.username] = self.replier(state=UserState.AUTHORIZED)

        if self.is_authorized(current_user.username):
            bot.send_message(chat_id=update.message.chat_id, text='Ты авторизован')
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Ты не авторизован, вызови /auth, '
                                                                  'чтобы получить инструкции')

    def auth_state(self, bot, update):
        current_user = MakeUser.from_telegram(update.message.from_user)
        if self.auth.is_authorized(current_user.username):
            bot.send_message(chat_id=update.message.chat_id,
                             text='Ты уже авторизован, поэтому нет смысла вызывать эту команду ;)')
            return
        if current_user.username not in self.auth_requested:
            self.auth_requested.add(current_user.username)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Чтобы начать спрашивать у меня про конференцию - введи пароль доступа к ней, '
                              'хотя ты можешь отправить и просто фотографию с qr кодом')

    def reply_handler(self, bot, update):
        current_user = MakeUser.from_telegram(update.message.from_user)
        if self.is_authorized(current_user.username):
            self.__reply(current_user, bot, update)
            return

        if current_user.username in self.auth_requested:
            self.__authorization(current_user, bot, update)
            return

        else:
            self.__default_process(current_user, bot, update)

    def button_callback(self, bot, update):
        query = update.callback_query
        user = MakeUser.from_telegram(query.from_user)
        self.__create_and_send_back_auth(query.data, user, bot, update)

    def launch(self):
        start_handler = CommandHandler('start', self.start_state)
        auth_handler = CommandHandler('auth', self.auth_state)
        reply_handler = MessageHandler(Filters.text, self.reply_handler)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(auth_handler)
        dispatcher.add_handler(reply_handler)

        dispatcher.add_handler(CallbackQueryHandler(self.button_callback))

        updater.start_polling()

    def __reply(self, user: User, bot, update):
        self.__create_and_send_back_auth(update.message.text, user, bot, update)

    def __authorization(self, user: User, bot, update):
        typed_password = update.message.text
        if self.complete_register(user, typed_password):
            bot.send_message(chat_id=update.message.chat_id, text='Круто, пароль принят!')
            self.user_repliers[user.username].set_user_state(UserState.AUTHORIZED)
            self.auth_requested.remove(user.username)
            self.__create_and_send_back_auth('Welcome', user, bot, update)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Произошла ошибка - пароль непринят\n '
                                                                  'Чтобы попробовать еще раз - вновь напиши /auth')
            self.auth_requested.remove(user.username)

    def __default_process(self, user: User, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='Функционал для не авторизованных')
        # TODO функционал для неавторизованных

    def __create_and_send_back_auth(self, ready_query: str, user: User, bot, update):
        where_to_search = self.get_conference_by_user_name(user.username)
        replier = self.user_repliers[user.username]

        user_request = QueryRequest(user, ready_query, where_to_search)
        analyzer_reply = self.analyzer.analyze(user_request)

        replier.create_reply(analyzer_reply, [bot, update])


if __name__ == '__main__':
    _= Alchemy.get_instance('../../db/data.db')
    em = EventManager()
    em.load_conference(1)
    auth = Auth()
    b = Bot(em, auth, TelegramReplier)
    b.launch()
    print('LETS RUN')
