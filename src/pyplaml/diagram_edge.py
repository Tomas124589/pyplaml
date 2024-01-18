from __future__ import annotations

from manim import *

from .diagram import Diagram
from .diagram_object import DiagramObject
from .relation import Relation


class DiagramEdge(DiagramObject):

    def __init__(self,
                 dotted: bool,
                 ):
        DiagramObject.__init__(self, "")
        self.dotted = dotted

        self.source: DiagramObject | None = None
        self.source_rel_type: Relation = Relation.NONE
        self.target: DiagramObject | None = None
        self.target_rel_type: Relation = Relation.NONE

        self.source_text = ""
        self.text = ""
        self.target_text = ""

        self.arrow_from_source = None

        self.mo_line: Line | None = None
        self.mo_src_text: Text | None = None
        self.mg_mid_text = VGroup()
        self.mo_mid_text_arrow: RegularPolygon | None = None
        self.mo_target_text: Text | None = None

    def between(self, source: DiagramObject, target: DiagramObject):
        self.source = source
        self.target = target
        return self

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

        always_redraw(self.line_updater)

        self.mobject = VGroup(self.mo_line)
        self.__prepare_mid_text()
        self.__prepare_src_text()
        self.__prepare_target_text()

        self.mo_line.add_updater(self.updater, call_updater=True)

        return self.mobject

    def __prepare_target_text(self):
        if self.target_text:
            self.mo_target_text = Text(self.target_text, color=BLACK).scale(0.75)
            self.mo_target_text.next_to(self.mo_line.get_end() - self.mo_target_text.height, LEFT, buff=0)
            self.mobject.add(self.mo_target_text)

    def __prepare_src_text(self):
        if self.source_text:
            self.mo_src_text = Text(self.source_text, color=BLACK).scale(0.75)
            self.mo_src_text.next_to(self.mo_line.get_start() + self.mo_src_text.height, RIGHT, buff=0)
            self.mobject.add(self.mo_src_text)

    def __prepare_mid_text(self):
        if self.text or self.arrow_from_source is not None:
            self.mg_mid_text = VGroup(Text(self.text, color=BLACK).scale(0.75))

            if self.arrow_from_source is not None:
                self.mo_mid_text_arrow = RegularPolygon(n=3, color=BLACK, fill_opacity=1)
                self.mo_mid_text_arrow.scale_to_fit_width(0.1)
                self.mo_mid_text_arrow.stretch_to_fit_height(self.mg_mid_text.height or 0.1)

                self.__set_mid_arrow_angle()

                self.mg_mid_text.add(self.mo_mid_text_arrow)

            self.mobject.add(
                self.mg_mid_text.arrange(LEFT, buff=0.1).next_to(self.mo_line.get_center(), RIGHT, buff=0.1))

    def __set_mid_arrow_angle(self):
        p1 = self.target.mobject.get_center()
        p2 = self.source.mobject.get_center()
        angle_to_obj = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
        if not self.arrow_from_source:
            angle_to_obj += 180 * DEGREES
        self.mo_mid_text_arrow.rotate(self.mo_mid_text_arrow.start_angle + angle_to_obj)

    def line_updater(self):
        (start, target) = self.get_closest_points()

        self.mo_line = DashedLine(buff=0, stroke_width=1, tip_length=0.25, color=BLACK) if self.dotted \
            else Line(buff=0, stroke_width=1, tip_length=0.25, color=BLACK)
        self.mo_line.put_start_and_end_on(start, target)

        self.__prepare_line_tips()

        return self.mo_line

    def updater(self, _: Mobject):
        if self.mo_src_text:
            self.mo_src_text.next_to(self.mo_line.get_start() + self.mo_src_text.height, RIGHT, buff=0)

        if self.mg_mid_text:
            self.mg_mid_text.next_to(self.mo_line.get_center(), RIGHT, buff=0.1)

        if self.mo_target_text:
            self.mo_target_text.next_to(self.mo_line.get_end() - self.mo_target_text.height, LEFT, buff=0)

    def get_closest_points(self):
        min_dist = float('inf')
        points = (None, None)

        weight_map = {
            'UL': 0.05, 'UR': 0.05, 'DL': 0.05, 'DR': 0.05,
            'UP': 0, 'R': 0, 'D': 0, 'L': 0,
        }

        for n1, p1 in self.source.get_boundary_points().items():
            w1 = weight_map[n1]

            for n2, p2 in self.target.get_boundary_points().items():
                w2 = weight_map[n2]

                dist = (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2
                dist += w1 + w2
                if dist < min_dist:
                    min_dist = dist
                    points = (p1, p2)

        return points

    def __prepare_line_tips(self):
        _dir = self.get_dir()
        def_params = {"tip_length": 0.2, "tip_width": 0.2}

        if _dir == -1:
            self.mo_line.add_tip(self.get_line_tip(self.source_rel_type), **def_params)

        elif _dir == 1:
            self.mo_line.add_tip(self.get_line_tip(self.target_rel_type), **def_params)

        elif _dir == 0:
            if self.dotted:
                self.mo_line.add_tip(self.get_line_tip(self.source_rel_type), **def_params)
                self.mo_line.add_tip(self.get_line_tip(self.target_rel_type), **def_params, at_start=True)

            else:
                self.mo_line.add_tip(self.get_line_tip(self.target_rel_type), **def_params, at_start=True)
                self.mo_line.add_tip(self.get_line_tip(self.source_rel_type), **def_params)

    @staticmethod
    def get_line_tip(rel: Relation):
        if rel == Relation.EXTENSION:
            return ArrowTriangleTip(color=BLACK, stroke_width=2, length=0.2, width=0.2)

        elif rel == Relation.ASSOCIATION:
            return StealthTip(color=BLACK, stroke_width=2, length=0.2)

        elif rel == Relation.AGGREGATION:
            return ArrowSquareTip(color=BLACK, stroke_width=2, length=0.15)

        elif rel == Relation.COMPOSITION:
            return ArrowSquareFilledTip(color=BLACK, stroke_width=2, length=0.15)

        elif rel == Relation.HASH:
            return ArrowSquareTip(color=BLACK, stroke_width=2, length=0.15)

    def append_to_diagram(self, diagram: Diagram) -> DiagramEdge:
        self.name = self.source.get_key() + "-" + self.source_rel_type.name + "-" + self.target_rel_type.name + "-" + self.target.get_key()
        DiagramObject.append_to_diagram(self, diagram)
        return diagram[self.name]