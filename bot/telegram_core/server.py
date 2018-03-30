import logging

from bot.service.abstract_bot import AbstractBot
from bot.telegram_core.keys import KEY

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=KEY)
dispatcher = updater.dispatcher


class Bot(AbstractBot):

    def start_state(self, bot, update):
        print(type(update.message.from_user))
        bot.send_message(chat_id=update.message.chat_id, text='Hello, world!')

    def launch(self):
        start_handler = CommandHandler('start', self.start_state)
        dispatcher.add_handler(start_handler)
        updater.start_polling()


if __name__ == '__main__':
    b = Bot()
    b.launch()
