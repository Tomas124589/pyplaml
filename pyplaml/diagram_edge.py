from manim import *

from .diagram import Diagram
from .diagram_object import DiagramObject
from .relation import Relation


class DiagramEdge(DiagramObject):

    def __init__(self,
                 dashed: bool,
                 size: int,
                 ):
        DiagramObject.__init__(self, '')
        self.dashed = dashed
        self.size = size

        self.source: DiagramObject | None = None
        self.source_rel_type = Relation.NONE
        self.target: DiagramObject | None = None
        self.target_rel_type = Relation.NONE

        self.source_text = ""
        self.text = ""
        self.target_text = ""

        self.arrow_from_source = None

    def get_dir(self):
        is_left = self.source_rel_type != Relation.NONE
        is_right = self.target_rel_type != Relation.NONE

        if is_left and is_right:
            return 0
        elif is_left:
            return -1
        elif is_right:
            return 1
        else:
            return None

    def predraw(self):
        if self.source.mobject is None or self.target.mobject is None \
                or self.source.is_hidden or self.target.is_hidden:
            return VGroup()

        start = self.source.mobject.get_center()
        target = self.target.mobject.get_center()

        direction = target - start
        direction /= np.linalg.norm(direction)
        direction = direction.round(0)

        start = self.source.mobject.get_critical_point(direction)
        target = self.target.mobject.get_critical_point(-direction)

        line = DashedLine(start, target, buff=0, stroke_width=1, tip_length=0.25) if self.dashed else Line(
            start, target, buff=0, stroke_width=1, tip_length=0.25)

        line.color = BLACK

        _dir = self.get_dir()
        if _dir == -1:
            line.add_tip(self.get_line_tip(self.source_rel_type))

        elif _dir == 1:
            line.add_tip(self.get_line_tip(self.target_rel_type))

        elif _dir == 0:
            line.add_tip(self.get_line_tip(self.target_rel_type))
            line.add_tip(self.get_line_tip(self.source_rel_type), at_start=True)

        group = VGroup(line)

        if self.text or self.arrow_from_source is not None:
            t_group = VGroup(Text(self.text, color=BLACK).scale(0.75))

            if self.arrow_from_source is not None:
                arrow = RegularPolygon(n=3, color=BLACK, fill_opacity=1)
                arrow.scale_to_fit_width(0.1)
                arrow.stretch_to_fit_height(t_group.height or 0.1)

                p1 = self.target.mobject.get_center()
                p2 = self.source.mobject.get_center()
                angle_to_obj = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])

                if not self.arrow_from_source:
                    angle_to_obj += 180 * DEGREES

                arrow.rotate(arrow.start_angle + angle_to_obj)

                t_group.add(arrow)

            group.add(t_group.arrange(LEFT, buff=0.1).next_to(line.get_center(), RIGHT, buff=0.1))

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

    def append_to_diagram(self, diagram: Diagram) -> DiagramObject:
        self.name = self.source.get_key() + "-" + self.source_rel_type.name + "-" + self.target_rel_type.name + "-" + self.target.get_key()
        return DiagramObject.append_to_diagram(self, diagram)
