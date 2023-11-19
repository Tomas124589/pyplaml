from __future__ import annotations

from abc import ABC, abstractmethod

from manim import *


class DiagramObject(ABC):

    def __init__(self, name: str):
        self.name = name
        self.mobject: Mobject | None = None

        self.x = 0
        self.y = 0

    @abstractmethod
    def draw(self) -> Mobject:
        pass
