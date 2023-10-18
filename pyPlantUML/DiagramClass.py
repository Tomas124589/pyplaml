from . import *

from manim import *


class DiagramClass(DiagramObject):

    def __init__(self, name: str, type: str):
        super().__init__(name)
        self.type = type

    def draw(self):

        header = Rectangle(color=GRAY)

        text = Text(self.name, color=BLACK, font_size=24)
        header.surround(text)

        propertyBody = Rectangle(color=GRAY, height=0.2, width=header.width)
        propertyBody.next_to(header, DOWN, buff=0)

        methodBody = Rectangle(color=GRAY, height=0.2, width=header.width)
        methodBody.next_to(propertyBody, DOWN, buff=0)

        self.mobject = VGroup(header, text, propertyBody, methodBody)

        return self.mobject
