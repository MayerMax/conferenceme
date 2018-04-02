from typing import Union

from bot.query import QueryResult


class Record:
    def __init__(self, vertex_name, request, query_result, previous=None):
        self.vertex_name = vertex_name
        self.request = request
        self.query_result = query_result
        self.previous = previous

    def previous(self) -> object:
        return self.previous


class Context:
    """
    класс, который хранит историю запросов и ответов пользователю
    """

    def __init__(self, user_name: str):
        self.__username = user_name
        self.__history = []

    def has_story(self):
        return len(self.__history) > 0

    def add_record(self, vertex_name: str, request: str, query_result: QueryResult):
        """
        добавляет запись в контекст пользователя
        :param vertex_name:
        :param request:
        :param query_result:
        :return:
        """
        record = Record(vertex_name, request, query_result, self)
        old_peek = self.peek()
        if old_peek:
            record.previous = old_peek
            self.__history.append(record)
        else:
            self.__history.append(record)

    def peek(self) -> Union[Record, None]:
        if not self.__history:
            return None
        return self.__history[-1]
