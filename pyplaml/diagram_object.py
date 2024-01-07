from __future__ import annotations

from abc import ABC, abstractmethod

from manim import *

import pyplaml


class DiagramObject(ABC):

    def __init__(self, name: str):
        self.name = name
        self.alias = None
        self.mobject: VMobject | None = None
        self.is_hidden = False
        self.do_draw = True

    def draw(self) -> VMobject:
        self.mobject = self.predraw()
        self.postdraw()
        return self.mobject

    @abstractmethod
    def predraw(self) -> VMobject:
        pass

    def postdraw(self) -> VMobject:
        if self.is_hidden:
            self.mobject.set_opacity(0)

        return self.mobject

    def add_critical_points(self):
        if self.mobject is not None:
            critical_points = [
                self.mobject.get_critical_point(direction=UL),
                self.mobject.get_critical_point(direction=UP),
                self.mobject.get_critical_point(direction=UR),
                self.mobject.get_critical_point(direction=LEFT),
                self.mobject.get_critical_point(direction=LEFT),
                self.mobject.get_critical_point(direction=ORIGIN),
                self.mobject.get_critical_point(direction=RIGHT),
                self.mobject.get_critical_point(direction=DL),
                self.mobject.get_critical_point(direction=DOWN),
                self.mobject.get_critical_point(direction=DR),
            ]
            self.mobject.add(VGroup(*[Dot(point, color=RED) for point in critical_points]))

    def append_to_diagram(self, diagram: pyplaml.Diagram) -> DiagramObject:
        key = self.get_key()
        if key not in diagram.objects:
            diagram[key] = self
        return diagram[key]

    def get_key(self):
        return self.alias or self.name

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self):
        return '({}) "{}", hidden: {}, draw: {}'.format(
            self.__class__.__name__,
            self.get_key() or 'NAME NOT SET',
            'yes' if self.is_hidden else 'no',
            'yes' if self.do_draw else 'no',
        )


class PositionedDiagramObject(DiagramObject):

    def __init__(self, name: str):
        super().__init__(name)
        self.x = 0
        self.y = 0

    @abstractmethod
    def predraw(self) -> VMobject:
        pass

    def postdraw(self) -> VMobject:
        super().postdraw()
        self.mobject.shift(RIGHT * self.x + DOWN * self.y)
        return self.mobject
