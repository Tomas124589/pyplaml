from . import *

from manim import *

class DiagramLine(DiagramObject):

    def __init__(self, name: str, source: DiagramObject, target: DiagramObject):
        DiagramObject.__init__(self, name)
        self.source = source
        self.target = target
        self.doCustomPosition = True

    def draw(self):
        line = Arrow(self.target.mobject.get_top(), self.source.mobject.get_bottom(), buff=0)
        line.color = BLACK

        self.mobject = line

        return self.mobject