from manim import *

from .diagram_object import DiagramObject


class Diagram:

    def __init__(self, name: str):
        self.scene: Scene | None = None
        self.name = name
        self.animate = False
        self.objects: typing.Dict[str, DiagramObject] = {}
        self.tagged: typing.Dict[str, set[DiagramObject]] = {}
        self.last_object: DiagramObject | None = None

    def __setitem__(self, key: str, val: DiagramObject):
        if not isinstance(val, DiagramObject):
            raise Exception('Only DiagramObject is allowed.')
        self.objects[key] = val
        self.last_object = val

    def __getitem__(self, key: str):
        return self.objects[str(key)]

    def objects_by_type(self, obj_type: str = ''):
        res = {}
        for name, obj in self.objects.items():
            _type = type(obj).__name__

            if _type in res:
                res[_type][name] = obj
            else:
                res[_type] = {}
                res[_type][name] = obj

        return res[obj_type] if obj_type != '' else res

    def draw(self):
        for name, obj in self.objects.items():
            if obj.do_draw:
                self.draw_object(obj)

    def draw_object(self, obj: DiagramObject):
        if obj.mobject is None:
            mobject = obj.draw()
            if mobject:
                if self.animate:
                    self.scene.play(Create(mobject))
                    self.scene.play(self.scene.camera.auto_zoom(
                        self.scene.mobjects, margin=0.5))
                else:
                    self.scene.add(mobject)
                    self.scene.camera.auto_zoom(
                        self.scene.mobjects, margin=0.5, animate=False)

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
