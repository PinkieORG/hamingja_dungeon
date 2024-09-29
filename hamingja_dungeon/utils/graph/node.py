from __future__ import annotations

from typing import Any


class Node:
    def __init__(self, value: Any):
        self.value = value
        self.neighbours = []

    def add_neighbour(self, neighbour: Node) -> None:
        self.neighbours.append(neighbour)
