from .DiagramNode import DiagramNode

from manim import *


class Diagram(DiagramNode):

    def __init__(self, name: str):
        super().__init__(name)
        self.identityMap: typing.Dict[str, DiagramNode] = {}

    def draw(self):
        for n in self.nodes:
            print(n)

    def addNode(self, node: DiagramNode):

        if node.name in self.identityMap:
            self.identityMap[node.name].nodes += node.nodes
            self.identityMap[node.name].lines.update(node.lines)
        else:
            super().addNode(node)
            self.identityMap[node.name] = node

        for n in node.nodes:
            self.identityMap[n.name] = n

    def setScene(self, scene: Scene):
        self.scene = scene
