from .diagram_object import DiagramObject
from .relation import Relation

from manim import *


class DiagramEdge(DiagramObject):

    def __init__(self,
                 name: str,
                 dashed: bool,
                 size: int,
                 ):
        DiagramObject.__init__(self, name)
        self.dashed = dashed
        self.size = size

        self.source = None
        self.source_rel_type = Relation.NONE
        self.target = None
        self.target_rel_type = Relation.NONE

        self.source_text = ""
        self.text = ""
        self.target_text = ""

    def draw(self):

        if self.source.mobject is None:
            raise Exception("Start object \"{}\" has not been drawn.".format(self.source.name))
        elif self.target.mobject is None:
            raise Exception("Target object \"{}\" has not been drawn.".format(self.target.name))

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

        if self.target_rel_type != Relation.NONE:
            line.add_tip(self.get_line_tip(self.target_rel_type))

        if self.source_rel_type != Relation.NONE:
            line.add_tip(self.get_line_tip(self.source_rel_type), at_start=True)

        group = VGroup(line)

        if self.text:
            text = Text(self.text, color=BLACK).scale(0.75)
            text.next_to(line.get_center(), RIGHT, buff=0)
            group.add(text)

        if self.source_text:
            text = Text(self.source_text, color=BLACK).scale(0.75)
            text.next_to(line.get_start() + text.height, RIGHT, buff=0)
            group.add(text)

        if self.target_text:
            text = Text(self.target_text, color=BLACK).scale(0.75)
            text.next_to(line.get_end() - text.height, LEFT, buff=0)
            group.add(text)

        self.mobject = group

        return self.mobject

    @staticmethod
    def get_line_tip(rel: Relation):
        if rel == Relation.EXTENSION:

            return ArrowTriangleTip(color=BLACK, stroke_width=2, length=0.2, width=0.2)

        elif rel == Relation.ASSOCIATION:

            return StealthTip(color=BLACK, stroke_width=2, length=0.2)

        elif rel == Relation.AGGREGATION:

            return ArrowSquareTip(color=BLACK, stroke_width=2,
                                  length=0.15)

        elif rel == Relation.COMPOSITION:

            return ArrowSquareFilledTip(color=BLACK, stroke_width=2, length=0.15)

        elif rel == Relation.HASH:

            return ArrowSquareTip(color=BLACK, stroke_width=2, length=0.15)
