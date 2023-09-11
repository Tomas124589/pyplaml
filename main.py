from manim import *

import parser as p

class MainScene(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        with open('inputs/simple.puml', 'r') as file:
            input = file.read()

        res = p.parser.parse(input)

        res.drawDiag(self)
