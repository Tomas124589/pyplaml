from manim import *

import pyplaml
from .diagram_layout import DiagramLayout
from .diagram_object import DiagramObject


class Diagram(VGroup):
    """Container for diagram objects.

    Objects with duplicate names are merged into one,
    merging can be defined in method append_to_diagram in any DiagramObject.
    """

    def __init__(self, layout: DiagramLayout | None = None, **kwargs):
        super().__init__(**kwargs)
        self.layout = layout
        self.objects: typing.Dict[str, DiagramObject] = {}
        self.tagged: typing.Dict[str, set[DiagramObject]] = {}
        self.last_object: DiagramObject | None = None

        self.__layout_scale_x = 1
        self.__layout_scale_y = 1

        self.do_show_icons = True

    def add(self, *vmobjects: DiagramObject):
        """Adds objects to diagram. Checks duplicate names and merges them."""
        for o in vmobjects:
            exists = o.get_key() in self.objects
            o = o.append_to_diagram(self)
            if not exists:
                if isinstance(o, pyplaml.DiagramClass):
                    o.set_show_icon(self.do_show_icons)

                super().add(o)

    def apply_layout(self, scale_x: float = 1, scale_y: float = 1):
        """Applies provided layout. Edges are automatically redrawn, to match new DiagramObjects positions."""
        if self.layout is not None:
            self.__layout_scale_x = scale_x
            self.__layout_scale_y = scale_y

            positions = self.layout.apply(
                {k: v for k, v in self.objects.items() if
                 isinstance(v, pyplaml.DiagramClass | pyplaml.DiagramNote) and v.do_draw},
                scale_x,
                scale_y
            )
            for name, pos in positions.items():
                _pos = (pos[0], pos[1], 0)
                self[name].move_to(_pos)

            for name, pos in positions.items():
                for e in self[name].edges:
                    e.redraw()

    def objects_by_degree(self):
        """Returns dictionary of objects where key is their key and value their degree."""
        degrees = {}
        for _, o in self.objects.items():
            if hasattr(o, "edges"):
                if o.get_key() in degrees:
                    degrees[o.get_key()] += len(o.edges)
                else:
                    degrees[o.get_key()] = len(o.edges)

                for e in o.edges:
                    if e.target.get_key() in degrees:
                        degrees[e.target.get_key()] += 1
                    else:
                        degrees[e.target.get_key()] = 1

        return degrees

    def add_to_tagged(self, tag: str, obj: DiagramObject):
        """Adds object to specified tag. Objects can be later hidden/removed/shown by their tags."""
        if tag in self.tagged:
            self.tagged[tag].add(obj)
        else:
            self.tagged[tag] = set()
            self.tagged[tag].add(obj)

    def remove_by_tag(self, tag: str):
        """Removes all objects with specified tag from diagram. Removed objects are invisible and don't matter in diagram layout."""
        if tag in self.tagged:
            for o in self.tagged[tag]:
                self.remove_object(o.get_key())

    def restore_by_tag(self, tag: str):
        """Restores all previously removed objects by tag."""
        if tag in self.tagged:
            for o in self.tagged[tag]:
                self.restore_object(o.get_key())

    def hide_by_tag(self, tag: str):
        """Hides objects by tag. Hidden objects are invisible, but still matter in diagram layout."""
        if tag in self.tagged:
            for o in self.tagged[tag]:
                self.hide_object(o.get_key())

    def show_by_tag(self, tag: str):
        """Shows previously hidden objects by tag."""
        if tag in self.tagged:
            for o in self.tagged[tag]:
                self.show_object(o.get_key())

    def show_icons(self, show: bool):
        """Sets if icons of DiagramClass objects should be drawn."""
        self.do_show_icons = show
        for n, o in self.objects.items():
            if isinstance(o, pyplaml.DiagramClass):
                o.set_show_icon(show)

    def remove_unlinked(self):
        """Removes all objects with no inbound/outbound DiagramEdges. Removed objects are invisible and don't matter in diagram layout."""
        objects = self.objects_by_degree()
        if objects:
            for n, deg in objects.items():
                if deg == 0:
                    self.remove_object(n)

    def restore_unlinked(self):
        """Restores all objects with no inbound/outbound DiagramEdges."""
        objects = self.objects_by_degree()
        if objects:
            for n, deg in objects.items():
                if deg == 0:
                    self.restore_object(n)

    def hide_unlinked(self):
        """Hides all objects with no inbound/outbound DiagramEdges. Hidden objects are invisible, but still matter in diagram layout."""
        for n, deg in self.objects_by_degree().items():
            if deg == 0:
                self.hide_object(n)

    def show_unlinked(self):
        """Shows all objects with no inbound/outbound DiagramEdges."""
        for n, deg in self.objects_by_degree().items():
            if deg == 0:
                self.show_object(n)

    def hide_object(self, key: str):
        """Hides an object, object still matters in diagram layout."""
        self[key].set_opacity(0)

    def show_object(self, key: str):
        """Shows previously hidden object"""
        self[key].set_opacity(1)

    def remove_object(self, key: str):
        """Removes an object, object no longer matters in diagram layout."""
        self[key].do_draw = False
        self[key].set_opacity(0)
        self.remove(self[key])

    def restore_object(self, key: str):
        """Restores previously removed object"""
        self[key].do_draw = True
        self[key].set_opacity(1)
        self.add(self.objects.pop(key))

    def __setitem__(self, key: str, val: DiagramObject):
        if not isinstance(val, DiagramObject):
            raise Exception("Only DiagramObject can be added to Diagram.")
        self.objects[key] = val
        self.last_object = val

    def __getitem__(self, key: str):
        return self.objects[str(key)]
