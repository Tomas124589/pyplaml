from .DiagramObject import DiagramObject
from .Relation import Relation

from manim import *


class DiagramEdge(DiagramObject):

    def __init__(self, name: str, target: DiagramObject, dashed: bool, size: int, sourceArrowType: str, targetArrowType: str):
        DiagramObject.__init__(self, name)
        self.target = target
        self.dashed = dashed
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

        line = DashedLine(start, target, buff=0, stroke_width=1, tip_length=0.25) if self.dashed else Line(
            start, target, buff=0, stroke_width=1, tip_length=0.25)

        line.color = BLACK

        line.add_tip(self.getLineTip())

        self.mobject = line

        return self.mobject

    def getLineTip(self):
        
        if self.targetArrowType == Relation.EXTENSION:

            return ArrowTriangleTip(color=BLACK, stroke_width=2, length=0.2, width=0.2)

        elif self.targetArrowType == Relation.ASSOCIATION:

            return StealthTip(color=BLACK, stroke_width=2, length=0.2)

        elif self.targetArrowType == Relation.AGGREGATION:

            return ArrowSquareTip(color=BLACK, stroke_width=2,
                                  length=0.15)

        elif self.targetArrowType == Relation.COMPOSITION:

            return ArrowSquareFilledTip(color=BLACK, stroke_width=2, length=0.15)

        elif self.targetArrowType == Relation.HASH:

            return ArrowSquareTip(color=BLACK, stroke_width=2, length=0.15)

        else:
            return None

    def __str__(self):
        result = super().__str__()
        if self.dashed:
            result += ",dotted"
        result += ", size: " + str(self.size)
        result += ", sourceArrow: " + self.sourceArrowType + "'"
        result += ", targetArrow: '" + self.targetArrowType + "'"

        return result
