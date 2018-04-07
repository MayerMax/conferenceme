import abc
from typing import List, Tuple

from bot.query import QueryResult, QueryRequest
from bot.service.conference_plain_object import ConferencePlainObject
from bot.service.history import Context
from bot.statuses import StatusTypes


class ActionVertexParentExists(Exception):
    pass


class BaseActionVertex(metaclass=abc.ABCMeta):
    """
    Класс, представляющий функциональное ядро логики бота. Каждая вершина - состояние, в котором сейчас бот.
    Вершина определеяет, что бот делает на данном этапе. Результат применения вершины - вызов активационной
    функции
    """

    def __init__(self, name: str, status: StatusTypes, alternative_name: str = None, parent=None):
        """
        конструктор
        :param name: уникальное имя вершины
        :param parent: родительская вершина для данной, объект типа ActionVertex
        :param status: статус вершины, является ли она терминальной или промежуточной
        :param alternative_name: альтернативное имя вершины, которое используется для того, чтобы replier-ы могли
        отображть вершину пользователю
        """
        self.name = name
        self.status = status
        self.parent = parent
        self.children = set()
        self.alternative_name = name if not alternative_name else alternative_name
        self.to_roots = None

    def add_child(self, child_vertex):
        """
        добавляет данному состоянию доченреи состояния
        :param child_vertex: дочерняя вершина
        :return: None
        """
        self.children.add(child_vertex)

    def set_parent(self, parent_vertex):
        """
        Устанавливает данной вершине родителя
        :param parent_vertex: BaseActionVertex
        :return:
        """
        if self.parent:
            raise ActionVertexParentExists('This vertex has already have parent named {}'.format(self.parent))
        self.parent = parent_vertex

    def set_roots(self, roots: List[str]):
        self.to_roots = roots

    def __str__(self):
        return 'Vertex {}, It has children: {}'.format(self.name, ', '.join(x.alternative_name for x in self.children))

    def get_children_alternative_names(self) -> List[str]:
        return [x.alternative_name for x in self.children]

    def get_children_names(self) -> List[str]:
        return [x.name for x in self.children]

    def get_unique_name(self) -> str:
        """
        Возвращает имя вершины
        :return:
        """
        return self.name

    @abc.abstractmethod
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        """
        абстрактная функция, возвращающая результат запроса пользователя в соответствии с QueryResult
        :param request: запрос пользователя
        :param context: история пользователя
        :return: QueryResult и список дочерних вершин
        """
        pass

    @abc.abstractmethod
    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        """
        абстрактная функция, которая помогает текущему состоянию бота понять, подходит ли пользовательский ввод данных
        для активационной функции. Необходима для активационных функций, который ожидают ввод в виде имен, названий,
        естественных запросов и проч. Для детерменированных вершин устанавливать в True
        :param request:
        :param context: контекст пользователя
        :return: число от 0 до 1, выражает уверенность в том, что это именно та вершина
        """
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()


class DummyVertex(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        pass

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> float:
        return True
