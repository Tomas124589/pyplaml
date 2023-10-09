from __future__ import annotations

from abc import ABC, abstractmethod

from typing import List

from manim import *


class DiagramObject(ABC):

    def __init__(self, name: str):
        self.objects: List[DiagramObject] = []
        self.lines: List[DiagramLine] = []
        self.name = name
        self.mobject: Mobject = None
        self.doCustomPosition = False

    @abstractmethod
    def draw(self) -> Mobject:
        pass

    def addLine(self, line: DiagramLine):
        self.lines.append(line)

    def __str__(self):
        result = "Class: '" + self.__class__.__name__ + "'"
        result += ", Name: '" + self.name + "'"

        return result

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))