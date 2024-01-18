from manim import *

from .diagram_edge import DiagramEdge
from .diagram_object import PositionedDiagramObject


class DiagramNote(PositionedDiagramObject):

    def __init__(self, name: str, text: str):
        super().__init__(name)
        self.text = text.replace("\\n", "\n")
        self.do_draw = False  # TODO Prepare note drawing

        self.edges: List[DiagramEdge] = []

    def predraw(self) -> VMobject:
        rect = Rectangle(fill_color="#feffdd", fill_opacity=1, stroke_color="#8c8c83", stroke_width=1)
        text = Text(self.text, color=BLACK).scale(0.75)
        rect.stretch_to_fit_width(text.width + 0.1)
        rect.stretch_to_fit_height(text.height + 0.1)

        return VGroup(rect, text)