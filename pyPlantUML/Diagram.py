from .DiagramObject import DiagramObject

from manim import *


class Diagram():

    def __init__(self, name: str):
        self.name = name
        self.objects: typing.Dict[str, DiagramObject] = {}
        self.animate = False

    def setLayout(self):
        firstLevelNodes = list(self.objects.keys())
        for name, obj in self.objects.items():
            if len(obj.edges) != 0:
                firstLevelNodes.remove(obj.name)

        self.assignObjectCoordinates(firstLevelNodes, 0)

    def assignObjectCoordinates(self, nodes: list, y: int):

        if len(nodes) == 0:
            return

        nextNodes = []
        xRange = self.rangeAroundZero(len(nodes))
        for i, name in enumerate(nodes):
            self.objects[name].x = xRange[i]
            self.objects[name].y = y

            for _, obj in self.objects.items():
                for edge in obj.edges:
                    if edge.target.name == name:
                        nextNodes.append(obj.name)

        self.assignObjectCoordinates(nextNodes, y+1)

    def draw(self):

        self.setLayout()

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

            mobj.shift(RIGHT * obj.x * 2)
            mobj.shift(DOWN * obj.y * 2)

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
