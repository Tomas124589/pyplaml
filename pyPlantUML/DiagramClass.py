from .DiagramObject import DiagramObject
from .DiagramEdge import DiagramEdge
from .ClassAttribute import ClassAttribute

from manim import *


class DiagramClass(DiagramObject):

    def __init__(self, name: str, class_type: str):
        super().__init__(name)
        self.type = class_type
        self.edges: List[DiagramEdge] = []
        self.attributes: List[ClassAttribute] = []
        self.methods: List[ClassAttribute] = []

    def draw(self):

        header = Rectangle(color=GRAY)
        text = Text(self.name, color=BLACK)
        header.surround(text)
        head_group = VGroup(header, text)

        attr_body = Rectangle(color=GRAY, height=0.2, width=0.2)
        attr_group = VGroup(attr_body)
        if len(self.attributes) != 0:

            attrs = VGroup()
            for attr in self.attributes:
                text_group = VGroup(
                    Text(attr.modifier.value, color=BLACK).scale(0.75),
                    Text(attr.text, color=BLACK).scale(0.75)
                )

                text_group.arrange(RIGHT, buff=0.)
                attrs.add(text_group)

            attrs.arrange(DOWN, buff=0.1)
            attr_group.add(attrs)
            attr_body.surround(attrs, buff=0.2)
            attr_body.stretch_to_fit_height(attrs.height + 0.1)

        method_body = Rectangle(color=GRAY, height=0.2, width=0.2)
        method_group = VGroup(method_body)
        if len(self.methods) != 0:
            methods = VGroup()
            for method in self.methods:
                text_group = VGroup(
                    Text(method.modifier.value, color=BLACK).scale(0.75),
                    Text(method.text, color=BLACK).scale(0.75)
                )

                text_group.arrange(RIGHT, buff=0.1)
                methods.add(text_group)

            methods.arrange(DOWN, buff=0.1)
            method_group.add(methods)
            method_body.surround(methods, buff=0.2)
            method_body.stretch_to_fit_height(methods.height + 0.1)

        max_width = max(head_group.width, attr_group.width, method_group.width)

        header.stretch_to_fit_width(max_width)
        attr_body.stretch_to_fit_width(max_width)
        method_body.stretch_to_fit_width(max_width)

        attr_group.next_to(head_group, DOWN, buff=0)
        method_group.next_to(attr_group, DOWN, buff=0)

        self.mobject = VGroup(head_group, attr_group, method_group)

        return self.mobject

    def add_edge(self, edge: DiagramEdge):
        self.edges.append(edge)
