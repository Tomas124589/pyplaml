from .DiagramObject import DiagramObject

from manim import *


class Diagram(DiagramObject):

    def __init__(self, name: str):
        super().__init__(name)
        self.objects: typing.Dict[str, DiagramObject] = {}
        self.animate = False

    def setVerticalLayout(self):
        noDependence = list(self.objects.keys())
        for name, obj in self.objects.items():
            for edge in obj.edges:
                if edge.target.name in noDependence:
                    noDependence.remove(edge.target.name)

        for name in noDependence:
            self.assignY(self.objects[name], 0)

    def assignY(self, node: DiagramObject, y: int):
        node.y = y

        for edge in node.edges:
            edge.target.y = y + 1
            self.assignY(edge.target, y+1)

    def draw(self):

        self.setVerticalLayout()

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

            edgeCount = len(obj.edges)
            xRange = self.rangeAroundZero(edgeCount)
            for i, edge in enumerate(obj.edges):
                edge.target.x = edge.target.x + xRange[i]

            if DiagramObject.hasCycle(obj):
                raise Exception("Cycle found.")

            if self.animate:
                self.scene.play(Create(mobj))
            else:
                self.scene.add(mobj)

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
