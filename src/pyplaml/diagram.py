from manim import *

import pyplaml
from .diagram_layout import DiagramLayout
from .diagram_object import DiagramObject


class Diagram(VGroup):

    def __init__(self, layout: DiagramLayout | None = None, **kwargs):
        super().__init__(**kwargs)
        self.layout = layout
        self.objects: typing.Dict[str, DiagramObject] = {}
        self.tagged: typing.Dict[str, set[DiagramObject]] = {}
        self.last_object: DiagramObject | None = None

        self.hide_unlinked = False
        self.remove_unlinked = False
        self.hide_icons = False

    def add(self, *vmobjects: DiagramObject):
        for o in vmobjects:
            exists = o.get_key() in self.objects
            o = o.append_to_diagram(self)
            if not exists:
                super().add(o)

    def apply_layout(self, scale_x: float = 1, scale_y: float = 1):
        if self.layout is not None:
            positions = self.layout.apply(
                {k: v for k, v in self.objects.items() if isinstance(v, pyplaml.DiagramClass)},
                scale_x,
                scale_y
            )
            for name, pos in positions.items():
                _pos = (pos[0], pos[1], 0)
                self[name].move_to(_pos)

            for name, pos in positions.items():
                for e in self[name].edges:
                    e.redraw()

    def objects_degree(self):
        degrees = {}
        for n, o in self.objects.items():
            if hasattr(o, "edges"):
                if n in degrees:
                    degrees[n] += len(o.edges)
                else:
                    degrees[n] = len(o.edges)

                for e in o.edges:
                    if e.target.name in degrees:
                        degrees[e.target.name] += 1
                    else:
                        degrees[e.target.name] = 1

        return degrees

    def add_to_tagged(self, tag: str, obj: DiagramObject):
        if tag in self.tagged:
            self.tagged[tag].add(obj)
        else:
            self.tagged[tag] = set()
            self.tagged[tag].add(obj)

    def remove_by_tag(self, tag: str):
        if tag in self.tagged:
            for o in self.tagged[tag]:
                o.do_draw = False

    def restore_by_tag(self, tag: str):
        if tag in self.tagged:
            for o in self.tagged[tag]:
                o.do_draw = True

    def hide_by_tag(self, tag: str):
        if tag in self.tagged:
            for o in self.tagged[tag]:
                o.is_hidden = True

    def show_by_tag(self, tag: str):
        if tag in self.tagged:
            for o in self.tagged[tag]:
                o.is_hidden = False

    def __setitem__(self, key: str, val: DiagramObject):
        if not isinstance(val, DiagramObject):
            raise Exception("Only DiagramObject can be added to Diagram.")
        self.objects[key] = val
        self.last_object = val

    def __getitem__(self, key: str):
        return self.objects[str(key)]
