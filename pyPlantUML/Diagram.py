from .DiagramNode import DiagramNode

from manim import *


class Diagram(DiagramNode):

    def draw(self):
        return None

    def drawDiag(self, scene: Scene):
        for n in self.nodes:

            noSceneObjects = len(scene.mobjects)

            mobject = n.draw()

            mobject.to_edge(UP+LEFT)

            scene.add(mobject)
