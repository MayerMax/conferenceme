from typing import List

import emoji
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

from bot.query import QueryResult
from bot.service.repliers.abstract_replier import AbstractReplier
from bot.statuses import UserState, StatusTypes


class TelegramReplier(AbstractReplier):
    def create_reply(self, query_result: QueryResult, extra_args: List[object]):
        bot, update = extra_args
        if self.stack:
            chat_id, message_id = self.stack.pop()
            keyboard = [[InlineKeyboardButton(emoji.emojize(':heavy_check_mark:'), callback_data='NONE')]]
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            bot.editMessageReplyMarkup(chat_id=chat_id, message_id=message_id, reply_markup=markup)

        if query_result.status == StatusTypes.ROOT or query_result.status == StatusTypes.LEAF:
            markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True,
                                         keyboard=[[x] for x in query_result.extra_args])
        else:
            keyboard = [[
                InlineKeyboardButton(option, callback_data=option)] for option in query_result.extra_args]
            markup = InlineKeyboardMarkup(hide_keyboard=True, inline_keyboard=keyboard)
            if query_result.extra_args:
                self.stack.append((update.message.chat_id, update.message.message_id+1))

        for text, attachment in zip(query_result.answer, query_result.attachments):
            bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=markup)
            if attachment:
                bot.send_photo(chat_id=update.message.chat_id, photo=open(attachment, 'rb'))
