from typing import List

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from bot.query import QueryResult
from bot.service.repliers.abstract_replier import AbstractReplier
from bot.statuses import UserState, StatusTypes


class TelegramReplier(AbstractReplier):
    def create_reply(self, query_result: QueryResult, extra_args: List[object]):
        bot, update = extra_args

        if query_result.status == StatusTypes.ROOT or query_result.status == StatusTypes.LEAF:
            markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                         keyboard=[[x] for x in query_result.extra_args])
        else:
            markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(option, callback_data=option) for option in query_result.extra_args]])

        for text, attachment in zip(query_result.answer, query_result.attachments):
            bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=markup)
            if attachment:
                bot.send_photo(chat_id=update.message.chat_id, photo=open(attachment, 'rb'))
