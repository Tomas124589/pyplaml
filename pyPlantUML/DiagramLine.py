from . import *

from manim import *

class DiagramLine(DiagramObject):

    def __init__(self, name: str, target: DiagramObject, dotted: bool, size: int, sourceArrowType: str, targetArrowType: str):
        DiagramObject.__init__(self, name)
        self.target = target
        self.dotted = dotted
        self.size = size
        self.sourceArrowType = sourceArrowType
        self.targetArrowType = targetArrowType
        self.doCustomPosition = True

    def draw(self):
        line = Arrow(self.target.mobject.get_top(), self.source.mobject.get_bottom(), buff=0)
        line.color = BLACK

        self.mobject = line

        return self.mobject

    def __str__(self):
        result = super().__str__()
        if self.dotted: result += ",dotted"
        result += ", size: " + str(self.size)
        result += ", sourceArrow: " + self.sourceArrowType + "'"
        result += ", targetArrow: '" + self.targetArrowType + "'"

        return result