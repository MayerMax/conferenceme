from typing import Union, List

from bot.query import QueryResult, QueryRequest
from bot.service.history import Context
from bot.statuses import StatusTypes
from bot.terminated_core.vertex.vertex import BaseActionVertex, DummyVertex


class NoSuchActionVertexInGraph(Exception):
    pass


class StateGraph:
    def __init__(self):
        self.vertices = {}
        self.default_vertices = set()

    def add_action_vertex(self, vertex: BaseActionVertex) -> None:
        """
        добавление вершины в граф, хранеине в self.vertices имени вершины
        :param vertex: BaseActionVertex
        :return: None
        """
        self.vertices[vertex.name] = vertex

    def get_action_vertex(self, name: str) -> Union[BaseActionVertex, None]:
        """
        возвращает вершину графа по имени (по естественному названию)
        :param name: имя вершины
        :return: BaseActionVertex или None, если такой вершины не нашлось
        """
        if name in self.vertices:
            return self.vertices[name]
        return None

    def add_transition_from_parent_to_child_by_names(self, parent_name: str, child_name: str):
        """
        создает отношение в графе между родительской вершиной и дочерней. Означает, что из вершины с именем
        parent_name можно перейти в вершину с именем child_name. Если одна из вершин отсутствует - исключение
        :param parent_name: имя родительской вершины
        :param child_name: имя дочерней вершины
        :return: None
        """
        parent_vertex = self.get_action_vertex(parent_name)
        child_vertex = self.get_action_vertex(child_name)
        if parent_vertex is None or child_vertex is None:
            raise NoSuchActionVertexInGraph('{} or {} does not exist in graph as vertex'.format(parent_name,
                                                                                                child_name))
        parent_vertex.add_child(child_name)
        child_vertex.set_parent(parent_name)

    def set_default_vertices(self, vertices_names: List[str]):
        self.default_vertices = set(vertices_names)

    def get_vertices_names(self) -> List[str]:
        """
        возвращает имена вершин графа
        :return: List[str]
        """
        return list(self.vertices.keys())

    def activate_vertex(self, vertex_name: str, request: QueryRequest, context: Context) -> QueryResult:
        vertex = self._vertex_exist_checker(vertex_name)
        return vertex.activation_function(request, context)

    def _vertex_exist_checker(self, vertex_name: str) -> BaseActionVertex:
        if vertex_name not in self.vertices:
            raise NoSuchActionVertexInGraph('vertex with name {} does not exist in the graph'.format(vertex_name))
        return self.vertices.get(vertex_name)
