from manim import *

from typing import Type

from pyPlantUML import *

import parser as p


class MainScene(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        with open(self.path, 'r') as file:
            input = file.read()

        diagram: Type[Diagram] = p.parser.parse(input)

        diagram.setScene(self)

        diagram.draw()

    def setInputPlantUml(self, path: str):
        self.path = path


if __name__ == "__main__":
    config.pixel_height = 720
    config.pixel_width = 1280
    config.save_as_gif = True
    config.cairo_path = "media/images/"
    config.ffmpeg_path = "media/videos/"

    if (len(sys.argv) > 1):
        scene = MainScene()
        scene.setInputPlantUml(sys.argv[1])
        scene.render()
    else:
        print("No input plant uml supplied")
