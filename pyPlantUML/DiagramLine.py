from . import *

from manim import *

class DiagramLine(DiagramNode):

    def __init__(self, name: str, source, target):
        DiagramNode.__init__(self, name)
        self.source = source
        self.target = target

    def draw(self):
        return Circle()