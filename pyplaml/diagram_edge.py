from .diagram_object import DiagramObject
from .relation import Relation

from manim import *


class DiagramEdge(DiagramObject):

    def __init__(self,
                 name: str,
                 source: DiagramObject,
                 target: DiagramObject,
                 dashed: bool,
                 size: int,
                 source_arrow_type: Relation,
                 target_arrow_type: Relation):
        DiagramObject.__init__(self, name)
        self.source = source
        self.target = target
        self.dashed = dashed
        self.size = size
        self.sourceArrowType = source_arrow_type
        self.targetArrowType = target_arrow_type

    def draw(self):

        start = self.source.mobject.get_top()
        target = self.target.mobject.get_bottom()

        if self.source.mobject.get_top()[1] > self.target.mobject.get_bottom()[1]:
            start = self.source.mobject.get_bottom()
            target = self.target.mobject.get_top()

        start_center = self.source.mobject.get_center()
        target_center = self.target.mobject.get_center()

        if self.source.y == self.target.y:
            if start_center[0] < target_center[0]:
                start = self.source.mobject.get_right()
                target = self.target.mobject.get_left()
            else:
                start = self.source.mobject.get_left()
                target = self.target.mobject.get_right()

        line = DashedLine(start, target, buff=0, stroke_width=1, tip_length=0.25) if self.dashed else Line(
            start, target, buff=0, stroke_width=1, tip_length=0.25)

        line.color = BLACK

        line.add_tip(self.get_line_tip())

        self.mobject = line

        return self.mobject

    def get_line_tip(self):

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
