from manim import *

from typing import Type

from pyPlantUML import *

import parser as p


class MainScene(MovingCameraScene):

    def construct(self):

        with open(self.path, 'r') as file:
            input = file.read()

        diagram: Type[Diagram] = p.parser.parse(input)

        diagram.setScene(self)

        diagram.animate = True

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
