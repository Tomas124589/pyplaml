from .DiagramObject import DiagramObject

from manim import *


class Diagram:

    def __init__(self, name: str):
        self.scene = None
        self.name = name
        self.objects: typing.Dict[str, DiagramObject] = {}
        self.animate = False

    def draw(self):

        for name, obj in self.objects.items():
            self.draw_object(obj)

        for name, obj in self.objects.items():
            for i, edge in enumerate(obj.edges):

                if self.animate:
                    self.scene.play(Create(edge.draw()))
                else:
                    self.scene.add(edge.draw())

    def draw_object(self, obj: DiagramObject):

        if obj.mobject is None:
            mobject = obj.draw()

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

    def add_object(self, obj: DiagramObject):

        if obj.name not in self.objects:
            self.objects[obj.name] = obj

            for edge in obj.edges:
                if edge.target.name in self.objects:
                    edge.target = self.objects[edge.target.name]
                else:
                    self.add_object(edge.target)
        else:
            for edge in obj.edges:
                if edge.target not in self.objects:
                    self.add_object(edge.target)
                edge.target = self.objects[edge.target.name]

            self.objects[obj.name].edges += obj.edges

    def set_scene(self, scene: Scene):
        self.scene = scene
