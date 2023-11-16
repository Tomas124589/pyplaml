from .DiagramObject import DiagramObject

from manim import *

class Diagram():

    def __init__(self, name: str):
        self.name = name
        self.objects: typing.Dict[str, DiagramObject] = {}
        self.animate = False

    def draw(self):

        for name, obj in self.objects.items():
            self.drawObject(obj)

        for name, obj in self.objects.items():
            for i, edge in enumerate(obj.edges):

                if self.animate:
                    self.scene.play(Create(edge.draw(obj)))
                else:
                    self.scene.add(edge.draw(obj))

    def drawObject(self, obj: DiagramObject):

        if obj.mobject is None:
            mobj = obj.draw()

            mobj.to_edge(UP)

            mobj.shift(RIGHT * obj.x)
            mobj.shift(DOWN * obj.y)

            if self.animate:
                self.scene.play(Create(mobj))
                self.scene.play(self.scene.camera.auto_zoom(
                    self.scene.mobjects, margin=0.5))
            else:
                self.scene.add(mobj)
                self.scene.camera.auto_zoom(
                    self.scene.mobjects, margin=0.5, animate=False)

    def addObject(self, obj: DiagramObject):

        if obj.name not in self.objects:
            self.objects[obj.name] = obj

            for edge in obj.edges:
                if edge.target.name in self.objects:
                    edge.target = self.objects[edge.target.name]
                else:
                    self.addObject(edge.target)
        else:
            for edge in obj.edges:
                if edge.target not in self.objects:
                    self.addObject(edge.target)
                edge.target = self.objects[edge.target.name]

            self.objects[obj.name].edges += obj.edges

    def rangeAroundZero(self, n):
        half_n = n // 2
        return list(range(-half_n, half_n + 1))

    def setScene(self, scene: Scene):
        self.scene = scene
