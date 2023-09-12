from . import *

from manim import *

class DiagramLine(DiagramNode):

    def __init__(self, name: str, source: DiagramNode, target: DiagramNode):
        DiagramNode.__init__(self, name)
        self.source = source
        self.target = target
        self.doCustomPosition = True

    def draw(self):
        line = Arrow(self.target.mobject.get_top(), self.source.mobject.get_bottom(), buff=0)
        line.color = BLACK

        return line