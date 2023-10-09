from __future__ import annotations

from abc import ABC, abstractmethod

from typing import List

from manim import *


class DiagramObject(ABC):

    def __init__(self, name: str):
        self.name = name
        self.mobject: Mobject = None
        self.doCustomPosition = False

    @abstractmethod
    def draw(self) -> Mobject:
        pass

    def __str__(self):
        result = "<" + self.__class__.__name__ + ">"
        result += ", Name: '" + self.name + "'"

        return result

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(str(self))