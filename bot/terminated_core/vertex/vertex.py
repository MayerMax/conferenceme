import abc


from bot.query import QueryResult
from bot.statuses import StatusTypes


class BaseActionVertex(metaclass=abc.ABCMeta):
    """
    Класс, представляющий функциональное ядро логики бота. Каждая вершина - состояние, в котором сейчас бот.
    Вершина определеяет, что бот делает на данном этапе. Результат применения вершины - вызов активационной
    функции
    """

    def __init__(self, name: str, status: StatusTypes, parent=None):
        """
        конструктор
        :param name: уникальное имя вершины
        :param parent: родительская вершина для данной, объект типа ActionVertex
        :param status: статус вершины, является ли она терминальной или промежуточной
        """
        self.name = name
        self.status = status
        self.parent = parent
        self.children = set()

    def add_child(self, child_name):
        """
        добавляет данному состоянию доченреи состояния
        :param child_name: дочерняя вершина
        :return: None
        """
        self.children.add(child_name)

    def __str__(self):
        return 'Vertex {}, It has children: {}'.format(self.name, ''.join(x.name for x in self.children))

    def get_unique_name(self) -> str:
        """
        Возвращает имя вершины
        :return:
        """
        return self.name

    @abc.abstractmethod
    def activation_function(self, user_raw_query, user_data, hierarchy, search_source) -> QueryResult:
        """
        абстрактная функция, возвращающая результат запроса пользователя в соответствии с QueryResult
        :param user_raw_query: исходный запрос пользователя, ВОЗМОЖНО, лишнее поле, так как в hierarchy хранится
        информация о предыдущем запросе
        :param user_data: информация о пользователе
        :param hierarchy: объект истории вызовов данного пользователя, нужен для обобщения логики, чтобы построить
        общий контекст
        :param search_source: место, в котором нужно искать данные
        :return: QueryResult
        """
        pass

    @abc.abstractmethod
    def predict_is_suitable_input(self, user_raw_query) -> bool:
        """
        абстрактная функция, которая помогает текущему состоянию бота понять, подходит ли пользовательский ввод данных
        для активационной функции. Необходима для активационных функций, который ожидают ввод в виде имен, названий,
        естественных запросов и проч. Для детерменированных вершин устанавливать в True
        :param user_raw_query:
        :return: True - да, допустим или False - нет, не ожидаемый формат
        """
        pass