from .diagram_object import DiagramObject

from manim import *


class Diagram:

    def __init__(self, name: str):
        self.scene: Scene | None = None
        self.name = name
        self.objects: typing.Dict[str, DiagramObject] = {}
        self.animate = False

    def __setitem__(self, key: str, obj: DiagramObject):
        self.objects[key] = obj

    def __getitem__(self, key: str):
        return self.objects[key]

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
        for name, obj in self.objects_by_type('DiagramClass').items():

            self.draw_object(obj)

        for name, obj in self.objects.items():
            if hasattr(obj, 'edges'):
                for i, edge in enumerate(obj.edges):
                    if self.animate:
                        self.scene.play(Create(edge.predraw()))
                    else:
                        self.scene.add(edge.predraw())

    def draw_object(self, obj: DiagramObject):
        if obj.mobject is None:
            mobject = obj.predraw()
            if mobject:
                mobject.to_edge(UP)
                mobject.shift(RIGHT * obj.x)
                mobject.shift(DOWN * obj.y)

                if self.animate:
                    self.scene.play(Create(mobject))
                    self.scene.play(self.scene.camera.auto_zoom(
                        self.scene.mobjects, margin=0.5))
                else:
                    self.scene.add(mobject)
                    self.scene.camera.auto_zoom(
                        self.scene.mobjects, margin=0.5, animate=False)

    def set_scene(self, scene: Scene):
        self.scene = scene
