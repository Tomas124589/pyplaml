from manim import *

from typing import Type

from pyPlantUML import *

import parser as p


class MainScene(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        # fPath = 'inputs/01_elements.puml'
        # fPath = 'inputs/02_relations.puml'
        # fPath = 'inputs/03_relations_extra.puml'
        # fPath = 'inputs/04_labels.puml'
        fPath = 'inputs/_test.puml'

        with open(fPath, 'r') as file:
            input = file.read()

        diagram: Type[Diagram] = p.parser.parse(input)

        diagram.setScene(self)

        diagram.draw()


if __name__ == "__main__":
    config.pixel_height = 720
    config.pixel_width = 1280
    config.save_as_gif = True
    config.cairo_path = "media/images/"
    config.ffmpeg_path = "media/videos/"

    scene = MainScene()
    scene.render()
