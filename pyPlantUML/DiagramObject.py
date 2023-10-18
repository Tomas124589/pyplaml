from __future__ import annotations

from abc import ABC, abstractmethod

from typing import List, TYPE_CHECKING

from manim import *

if TYPE_CHECKING:
    from .DiagramEdge import DiagramEdge


class DiagramObject(ABC):

    def __init__(self, name: str):
        self.name = name
        self.mobject: Mobject = None
        self.doCustomPosition = False
        self.edges: List[DiagramEdge] = []

        self.x = 0
        self.y = 0

    @abstractmethod
    def draw(self) -> Mobject:
        pass

    def addEdge(self, edge: DiagramEdge):
        self.edges.append(edge)

    def __str__(self):
        result = "<" + self.__class__.__name__ + ">"
        result += ", Name: '" + self.name + "'"

        return result

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))
