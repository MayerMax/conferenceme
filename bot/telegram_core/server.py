import logging

from bot.service.abstract_bot import AbstractBot
from bot.service.auth import Auth
from bot.service.event_manager import EventManager
from bot.service.repliers.telegram_replier import TelegramReplier
from bot.statuses import UserState
from bot.telegram_core.keys import KEY

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=KEY)
dispatcher = updater.dispatcher


class Bot(AbstractBot):
    def start_state(self, bot, update):
        current_user = update.message.from_user.username
        if self.is_authorized(current_user):
            pass  # TODO вершина для приветствия
            bot.send_message(chat_id=update.message.chat_id,
                             text='Уже авторизован!')
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Привет! Чтобы получить доступ к функционалу - авторизуйся через меня.'
                                  'Просто введи пароль к конференции.'
                                  'Или опробуй функции по умолчанию.')
            # TODO вершина для действий по умолчанию

    def reply(self, bot, update):
        current_user = update.message.from_user.username
        if self.is_authorized(current_user):
            self.__reply(bot, update)
        else:
            self.__check_auth_reply(bot, update)

    def launch(self):
        start_handler = CommandHandler('start', self.start_state)
        reply_handler = MessageHandler(Filters.text, self.reply)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(reply_handler)
        updater.start_polling()

    def __reply(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text='Вот мой ответ!')

    def __check_auth_reply(self, bot, update):
        current_user = update.message.from_user.username
        message = update.message.text
        if self.complete_register(current_user, message):
            self.user_repliers[current_user] = self.replier(state=UserState.AUTHORIZED)
            bot.send_message(chat_id=update.message.chat_id,
                             text='Супер, теперь я готов с тобой общаться!')
            # TODO вершина графа для приветствия
        else:
            self.user_repliers[current_user] = self.replier(state=UserState.GUEST)
            bot.send_message(chat_id=update.message.chat_id,
                             text='Для меня ты - гость, могу помочь с бронированием :)')
            # TODO вершина для действий по умолчанию


if __name__ == '__main__':
    em = EventManager()
    auth = Auth()
    b = Bot(em, auth, TelegramReplier)
    b.launch()
    print('LETS RUN')
