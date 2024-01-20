from abc import abstractmethod

from manim import *

from pyplaml import *


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

    def construct(self):
        self.settings()
        self.anims()

    def settings(self):
        self.camera.background_color = WHITE
        Text.set_default(font_size=16)
