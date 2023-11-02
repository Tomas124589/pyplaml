from .DiagramObject import DiagramObject

from manim import *


class DiagramClass(DiagramObject):

    def __init__(self, name: str, type: str):
        super().__init__(name)
        self.type = type
        self.attributes = []
        self.methods = []

    def draw(self):

        header = Rectangle(color=GRAY)
        text = Text(self.name, color=BLACK, font_size=16)
        header.surround(text)
        headGroup = VGroup(header, text)

        attrBody = Rectangle(color=GRAY, height=0.2, width=0.2)
        attrGroup = VGroup(attrBody)
        if len(self.attributes) != 0:

            attrs = VGroup()
            for attr in self.attributes:
                attrs.add(Text(attr, color=BLACK, font_size=12))

            attrs.arrange(DOWN, buff=0.1)
            attrGroup.add(attrs)
            attrBody.surround(attrs, buff=0.2)
            attrBody.stretch_to_fit_height(attrs.height + 0.1)

        methodBody = Rectangle(color=GRAY, height=0.2, width=0.2)
        methodGroup = VGroup(methodBody)
        if len(self.methods) != 0:
            methods = VGroup()
            for method in self.methods:
                methods.add(Text(method, color=BLACK, font_size=12))

            methods.arrange(DOWN, buff=0.1)
            methodGroup.add(methods)
            methodBody.surround(methods, buff=0.2)
            methodBody.stretch_to_fit_height(methods.height + 0.1)

        maxWidth = max(headGroup.width, attrGroup.width, methodGroup.width)

        header.stretch_to_fit_width(maxWidth)
        attrBody.stretch_to_fit_width(maxWidth)
        methodBody.stretch_to_fit_width(maxWidth)

        attrGroup.next_to(headGroup, DOWN, buff=0)
        methodGroup.next_to(attrGroup, DOWN, buff=0)

        self.mobject = VGroup(headGroup, attrGroup, methodGroup)

        return self.mobject
