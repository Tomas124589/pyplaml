from manim import *

from pyplaml import *

import argparse

from pyplaml.layout.spring_layout import SpringLayout
from pyplaml.layout.hierarchical_layout import HierarchicalLayout


class MainScene(MovingCameraScene):
    file: str
    animate: bool

    def construct(self):
        parser = PUMLParser()
        d: Diagram = parser.parse_file(self.file)

        layout = HierarchicalLayout(d)
        layout.apply()
        layout.scale(2, 2)

        self.camera.background_color = WHITE
        Text.set_default(font_size=16)

        d.set_scene(self)

        d.animate = self.animate

        d.draw()

    def set_file(self, file: str):
        self.file = file

    def set_animate(self, animate: bool):
        self.animate = animate


if __name__ == "__main__":
    config.output_file = "PlantUML"
    config.cairo_path = "media/images/"
    config.ffmpeg_path = "media/videos/"

    argparser = argparse.ArgumentParser(prog="pyplaml")

    argparser.add_argument("file")
    argparser.add_argument("-a", "--animate", action="store_true")

    args = argparser.parse_args()

    scene = MainScene()

    scene.set_file(args.file)
    scene.set_animate(args.animate)

    scene.render()
