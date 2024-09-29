from typing import Any, List

from utils.graph.node import Node


class Graph:
    def __init__(self):
        self.nodes: List[Node] = []

    def push(self, element: Any, neighbours: List[Any] = None) -> None:
        new_node = Node(element)
        for neighbour in neighbours:
            new_node.add_neighbour(neighbour)
        self.nodes.append(new_node)

    def add_neighbour_to(self, element: Any, neighbour: Any) -> None:
        for vertex in self.nodes:
            if vertex.value == element:
                vertex.add_neighbour(neighbour)

    def get_neighbours(self, element: Any) -> List[Any]:
        for vertex in self.nodes:
            if vertex.value == element:
                return vertex.neighbours
        return []
