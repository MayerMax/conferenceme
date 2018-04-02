from typing import List

from bot.service.conference_plain_object import ConferencePlainObject
from bot.service.users.user import User
from bot.statuses import StatusTypes


class QueryResult:
    """
    Класс, который формирует ответ, принимаемый интерфейсами для разных мессенджеров, чтобы отдать пользователю
    результат
    """

    def __init__(self, status: StatusTypes, answer: List[str], attachments: List[str], extra_args: object = None):
        """
        конструктор
        :param status: статус формируемого результата - конец ли это диалога или бот ожидает продолжение
        :param answer: ответ бота на запрос. Представляет из себя список строк. Бот может отправлять вложения любого
        типа(фото или аудио - пути до файлов), поэтому на каждый овтет может быть соответствующее вложение
        :param attachments: описание для поля answer
        :param extra_args: для непредвиденных ситуаций, которе могут быть обработаны только специфичным ботом
        """
        self.status = status
        self.answer = answer
        self.attachments = attachments
        self.extra_args = extra_args


class QueryRequest:
    """
    Класс, который формирует запрос, принимаемый интерфейсами для разных мессенджеров, чтобы отдать анализатору
    """

    def __init__(self, who_asked: User, question: str, where_to_search: ConferencePlainObject):
        """
        конструктор
        :param who_asked: пользователь мессенджера
        :param question: сырой запрос пользователя
        :param where_to_search: объект конференции, в котором осуществляется поиск
        """
        self.who_asked = who_asked
        self.question = question
        self.where_to_search = where_to_search