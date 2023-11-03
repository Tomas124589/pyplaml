from manim import *
from typing import Type

from pyPlantUML import *

import argparse


class MainScene(MovingCameraScene):

    def construct(self):

        parser = PUMLParser()
        diagram: Type[Diagram] = parser.parseFile(self.file)

        self.camera.background_color = WHITE
        Text.set_default(font_size=16)

        diagram.setScene(self)

        diagram.animate = self.animate

        diagram.draw()

    def setFile(self, file: str):
        self.file = file

    def setAnimate(self, animate: bool):
        self.animate = animate


if __name__ == "__main__":
    config.output_file = "PlantUML"
    config.cairo_path = "media/images/"
    config.ffmpeg_path = "media/videos/"

    argparser = argparse.ArgumentParser(
        prog="pyPlantUML"
    )

    argparser.add_argument('-f', '--file', required=True,
                           type=str, help="Path to source plantUml file.")
    argparser.add_argument('-a', '--animate', action="store_true")

    args = argparser.parse_args()

    scene = MainScene()

    scene.setFile(args.file)
    scene.setAnimate(args.animate)

    scene.render()
