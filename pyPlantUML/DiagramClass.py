from .DiagramNode import DiagramNode

from manim import *


class DiagramClass(DiagramNode):

    def draw(self):

        header = Rectangle(color=GRAY)

        text = Text(self.name, color=BLACK)

        propertyBody = Rectangle(color=GRAY, height=0.2)
        propertyBody.next_to(header, DOWN, buff=0)

        methodBody = Rectangle(color=GRAY, height=0.2)
        methodBody.next_to(propertyBody, DOWN, buff=0)

        return VGroup(header, text, propertyBody, methodBody)