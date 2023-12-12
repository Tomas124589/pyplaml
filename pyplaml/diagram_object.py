from __future__ import annotations

from abc import ABC, abstractmethod

from manim import *

import pyplaml


class DiagramObject(ABC):

    def __init__(self, name: str):
        self.name = name
        self.mobject: VMobject | None = None

        self.x = 0
        self.y = 0

    @abstractmethod
    def draw(self) -> VMobject:
        pass

    def append_to_diagram(self, diagram: pyplaml.Diagram) -> DiagramObject:
        if self.name not in diagram.objects:
            diagram[self.name] = self
        return diagram[self.name]
