from .DiagramObject import DiagramObject

from manim import *


class DiagramEdge(DiagramObject):

    def __init__(self, name: str, target: DiagramObject, dotted: bool, size: int, sourceArrowType: str, targetArrowType: str):
        DiagramObject.__init__(self, name)
        self.target = target
        self.dotted = dotted
        self.size = size
        self.sourceArrowType = sourceArrowType
        self.targetArrowType = targetArrowType
        self.doCustomPosition = True

    def draw(self, source: DiagramObject):

        start = source.mobject.get_top()
        target = self.target.mobject.get_bottom()

        if source.mobject.get_top()[1] > self.target.mobject.get_bottom()[1]:
            start = source.mobject.get_bottom()
            target = self.target.mobject.get_top()

        startCenter = source.mobject.get_center()
        targetCenter = self.target.mobject.get_center()

        if source.y == self.target.y:
            if startCenter[0] < targetCenter[0]:
                start = source.mobject.get_right()
                target = self.target.mobject.get_left()
            else:
                start = source.mobject.get_left()
                target = self.target.mobject.get_right()

        line = Arrow(start, target, buff=0, stroke_width=1, tip_length=0.25)
        line.color = BLACK

        self.mobject = line

        return self.mobject

    def __str__(self):
        result = super().__str__()
        if self.dotted:
            result += ",dotted"
        result += ", size: " + str(self.size)
        result += ", sourceArrow: " + self.sourceArrowType + "'"
        result += ", targetArrow: '" + self.targetArrowType + "'"

        return result
