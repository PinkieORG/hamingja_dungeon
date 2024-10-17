import itertools
from typing import Any

import igraph as ig


class ObjectContainer:
    def __init__(self):
        self._graph = ig.Graph()
        self.id_generator = itertools.count()

    def _get_new_id(self) -> int:
        return next(self.id_generator)

    def _get_vertex_index(self, object_id: int) -> int:
        return self._graph.vs.find(id=object_id).index

    def _get_object_id(self, vertex: int) -> int:
        return self._graph.vs[vertex]["id"]

    def add_object(self, object: Any) -> int:
        new_id = self._get_new_id()
        self._graph.add_vertex(id=new_id, object=object)
        return new_id

    def add_object_with_data(self, object: Any, data: dict) -> int:
        new_id = self._get_new_id()
        self._graph.add_vertex(id=new_id, object=object, **data)
        return new_id

    def remove_object(self, object_id: int) -> None:
        vertex = self._get_vertex_index(object_id)
        self._graph.delete_vertices([vertex])

    def get_object(self, object_id: int) -> Any:
        vertex = self._get_vertex_index(object_id)
        return self._graph.vs[vertex]["object"]

    def get_all_objects(self) -> list[Any]:
        if self._graph.vcount() == 0:
            return []
        return list(self._graph.vs["object"])

    def get_all_object_ids(self) -> list[int]:
        if self._graph.vcount() == 0:
            return []
        return self._graph.vs.get_attribute_values("id")

    def get_object_data(self, object_id: int) -> dict:
        vertex = self._get_vertex_index(object_id)
        return self._graph.vs[vertex]

    def add_connection_with_data(
        self, first_object_id: int, second_object_id: int, data: dict
    ) -> None:
        first_vertex = self._get_vertex_index(first_object_id)
        second_vertex = self._get_vertex_index(second_object_id)
        self._graph.add_edge(first_vertex, second_vertex, **data)

    def get_connection_data(self, first_object_id: int, second_object_id: int) -> dict:
        first_vertex = self._get_vertex_index(first_object_id)
        second_vertex = self._get_vertex_index(second_object_id)
        edge = self._graph.get_eid(first_vertex, second_vertex)
        return self._graph.es[edge]

    def get_connected_objects(self, object_id: int) -> list[int]:
        vertex = self._get_vertex_index(object_id)
        neighbour_ids = []
        for neighbour_vertex in self._graph.neighbors(vertex):
            neighbour_ids.append(self._get_object_id(neighbour_vertex))
        return neighbour_ids
