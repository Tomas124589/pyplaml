from .DiagramObject import DiagramObject

from manim import *


class Diagram(DiagramObject):

    def __init__(self, name: str):
        super().__init__(name)
        self.identityMap: typing.Dict[str, DiagramObject] = {}

    def draw(self):
        for n in self.objects:
            print(n)

    def addObject(self, obj: DiagramObject):

        if obj.name in self.identityMap:
            self.identityMap[obj.name].objects += obj.objects
            self.identityMap[obj.name].lines.update(obj.lines)
        else:
            super().addObject(obj)
            self.identityMap[obj.name] = obj

        for n in obj.objects:
            self.identityMap[n.name] = n

    def setScene(self, scene: Scene):
        self.scene = scene
