from manim import *
from typing import Type

from PUMLParser import PUMLParser
from pyPlantUML import *


class MainScene(MovingCameraScene):

    def construct(self):

        parser = PUMLParser()
        diagram: Type[Diagram] = parser.parseFile(self.path)

        diagram.setScene(self)

        diagram.animate = False

        diagram.draw()

    def setInputPlantUml(self, path: str):
        self.path = path


if __name__ == "__main__":
    config.output_file = "PlantUML"
    config.background_color = WHITE
    config.cairo_path = "media/images/"
    config.ffmpeg_path = "media/videos/"

    if (len(sys.argv) > 1):
        scene = MainScene()
        scene.setInputPlantUml(sys.argv[1])
        scene.render()
    else:
        print("No input plant uml supplied")
