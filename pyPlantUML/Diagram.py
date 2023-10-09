from .DiagramObject import DiagramObject

from manim import *


class Diagram(DiagramObject):

    def __init__(self, name: str):
        super().__init__(name)
        self.objects: typing.Dict[str, DiagramObject] = {}

    def draw(self):
        for o in self.objects:
            self.drawObject(o, 0, 0)

    def drawObject(self, obj: DiagramObject, x: int, y: int):

        mobj = obj.draw()

        mobj.to_edge(UP)
        mobj.shift(RIGHT * 2 * x)
        mobj.shift(DOWN * 2 * y)

        self.scene.add(mobj)

        x = len(obj.objects) * -0.5 + 0.5
        y += 1

        for o in obj.objects:
            self.drawObject(o, x, y)
            x += 1

        for l in obj.lines:
            self.scene.add(l.draw())

    def addObject(self, obj: DiagramObject):

        if obj.name not in self.objects:
            self.objects[obj.name] = obj

    def setScene(self, scene: Scene):
        self.scene = scene
