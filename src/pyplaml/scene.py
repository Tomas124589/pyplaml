from abc import abstractmethod

from manim import *

from pyplaml import *
from pyplaml.diagram_layout import DiagramLayoutFactory


class Scene(MovingCameraScene):
    diagram: Diagram
    parser: PUMLParser = PUMLParser()
    animate: bool

    layout: str = ''
    scale_x: float
    scale_y: float

    @abstractmethod
    def anims(self):
        pass

    @abstractmethod
    def prepare_diagram(self) -> Diagram:
        pass

    def mo(self, key: str):
        return self.diagram.objects[key].mobject

    def moa(self, key: str):
        return self.mo(key).animate

    def construct(self):
        self.settings()

        self.diagram = self.prepare_diagram()
        self.diagram.scene = self

        if self.layout:
            DiagramLayoutFactory.make(self.layout, self.diagram).apply().scale(self.scale_x, self.scale_y)
        self.diagram.draw()

        self.anims()

    def settings(self):
        self.camera.background_color = WHITE
        Text.set_default(font_size=16)

    def set_layout(self, name: str, scale_x: float = 1, scale_y: float = 1):
        self.layout = name
        self.scale_x = scale_x
        self.scale_y = scale_y
