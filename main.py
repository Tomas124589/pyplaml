from manim import *

import parser as p

class MainScene(Scene):

    def construct(self):

        self.camera.background_color = WHITE

        with open('inputs/01_elements.puml', 'r') as file:
            input = file.read()

        diagram = p.parser.parse(input)

        diagram.setScene(self)

        diagram.draw()
