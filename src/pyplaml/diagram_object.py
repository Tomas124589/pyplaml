from __future__ import annotations

from abc import abstractmethod

from manim import *

import pyplaml


class DiagramObject(VGroup):

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.alias = None
        self.is_hidden = False
        self.do_draw = True
        self.notes: Dict[pyplaml.Direction, List[pyplaml.DiagramNote]] = {}

    @abstractmethod
    def redraw(self):
        self.submobjects = []

    def add_note(self, note: pyplaml.DiagramNote, direction: pyplaml.Direction) -> pyplaml.DiagramNote:
        if direction not in self.notes:
            self.notes[direction] = []

        self.notes[direction].append(note)

        self.redraw()

        return note

    def get_boundary_points(self):
        ul = self.get_boundary_point(direction=UL)
        ur = self.get_boundary_point(direction=UR)
        dl = self.get_boundary_point(direction=DL)
        dr = self.get_boundary_point(direction=DR)

        u = self.lerp(0.5, ul, ur)
        r = self.lerp(0.5, ur, dr)
        d = self.lerp(0.5, dl, dr)
        l = self.lerp(0.5, ul, dl)

        return {'UL': ul, 'UR': ur, 'UP': u, 'DL': dl, 'DR': dr, 'R': r, 'D': d, 'L': l, }

    @staticmethod
    def lerp(t: float, a, b):
        return (1 - t) * a + t * b

    def append_to_diagram(self, diagram: pyplaml.Diagram):
        key = self.get_key()
        if not key in diagram.objects:
            diagram[key] = self
        return self

    def get_key(self):
        return self.alias or self.name

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self):
        return "({}) \"{}\", hidden: {}, draw: {}".format(
            self.__class__.__name__,
            self.get_key() or "NAME NOT SET",
            "yes" if self.is_hidden else "no",
            "yes" if self.do_draw else "no",
        )
