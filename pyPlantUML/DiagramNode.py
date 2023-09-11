from __future__ import annotations

from abc import ABC, abstractmethod

from typing import List

from manim import *


class DiagramNode(ABC):

    def __init__(self, name: str):
        self.nodes: List[DiagramNode] = []
        self.name = name

    @abstractmethod
    def draw(self) -> Mobject:
        pass

    def addNode(self, node: DiagramNode):
        self.nodes.append(node)

    def __str__(self):
        result = self.__class__.__name__ + "\n"
        result += "Name: " + self.name + "\n"
        result += "No of nodes: " + str(len(self.nodes)) + "\n"

        return result
