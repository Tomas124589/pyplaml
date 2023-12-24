from __future__ import annotations

from abc import ABC, abstractmethod

from manim import *

import pyplaml


class DiagramObject(ABC):

    def __init__(self, name: str):
        self.name = name
        self.alias = None
        self.mobject: VMobject | None = None

        self.x = 0
        self.y = 0

    @abstractmethod
    def predraw(self) -> VMobject:
        pass

    def append_to_diagram(self, diagram: pyplaml.Diagram) -> DiagramObject:
        key = self.get_key()
        if key not in diagram.objects:
            diagram[key] = self
        return diagram[key]

    def get_key(self):
        return self.alias or self.name

    def __str__(self) -> str:
        return str(self.name)
