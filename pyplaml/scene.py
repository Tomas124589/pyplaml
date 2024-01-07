from abc import abstractmethod

from manim import *

from pyplaml import PUMLParser, Diagram
from pyplaml.diagram_layout import DiagramLayoutFactory


class Scene(MovingCameraScene):
    diagram: Diagram
    layout: str
    file: str
    animate: bool
    scale_x: float
    scale_y: float

    @abstractmethod
    def anims(self):
        pass

    def mo(self, key: str):
        return self.diagram.objects[key].mobject

    def moa(self, key: str):
        return self.mo(key).animate

    def prepare_diagram(self):
        parser = PUMLParser()
        self.diagram = parser.parse_file(self.file)
        self.diagram.scene = self
        self.diagram.animate = self.animate

        DiagramLayoutFactory.make(self.layout, self.diagram).apply().scale(self.scale_x, self.scale_y)

        self.diagram.draw()

    def settings(self):
        self.camera.background_color = WHITE
        Text.set_default(font_size=16)

    def construct(self):
        self.settings()
        self.prepare_diagram()
        self.anims()
