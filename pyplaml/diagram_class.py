from .diagram_object import DiagramObject
from .diagram_edge import DiagramEdge
from .class_attribute import ClassAttribute, AttributeModifier
from .diagram import Diagram
from .class_type import ClassType

from manim import *


class DiagramClass(DiagramObject):

    def __init__(self, name: str):
        super().__init__(name)
        self.edges: List[DiagramEdge] = []
        self.attributes: List[ClassAttribute] = []
        self.methods: List[ClassAttribute] = []
        self.is_abstract = False

    def append_to_diagram(self, diagram: Diagram) -> DiagramObject:
        if self.name not in diagram.objects:
            diagram[self.name] = self
            for edge in self.edges:
                if edge.target.name in diagram.objects:
                    edge.target = diagram[edge.target.name]
                else:
                    edge.target.append_to_diagram(diagram)
        else:
            for edge in self.edges:
                if edge.target not in diagram:
                    edge.target.append_to_diagram(diagram)
                edge.target = diagram[edge.target.name]
            diagram[self.name].edges += self.edges

        return diagram[self.name]

    def predraw(self):
        slant = ITALIC if self.is_abstract else NORMAL

        header = Rectangle(color=GRAY)
        text = Text(self.name, color=BLACK, slant=slant)
        header.surround(text, buff=0.8)
        head_group = VGroup(header, VGroup(self.prepare_icon(), text).arrange(RIGHT, buff=0.1))

        attr_body = Rectangle(color=GRAY, height=0.2, width=0.2)
        attr_group = VGroup(attr_body)
        if len(self.attributes) != 0:

            attrs = VGroup()
            for attr in self.attributes:
                text_group = VGroup(
                    Text(attr.modifier.value, color=BLACK),
                    Text(attr.text, color=BLACK)
                )

                text_group.arrange(RIGHT, buff=0.1).scale(0.75)
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
                    Text(method.modifier.value, color=BLACK),
                    Text(method.text, color=BLACK)
                )

                text_group.arrange(RIGHT, buff=0.1).scale(0.75)
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

    @staticmethod
    def get_icon(text: str, colour) -> VMobject:
        c = Circle(color=BLACK, fill_color=colour, stroke_width=2, fill_opacity=1)
        t = Text(text, color=BLACK)
        c.surround(t, buffer_factor=1.6)
        return VGroup(c, t)

    def prepare_icon(self):
        return self.get_icon('A' if self.is_abstract else 'C', TEAL if self.is_abstract else GREEN)

    def add_edge(self, edge: DiagramEdge):
        self.edges.append(edge)

    def add_attribute(self, attr_str: str):
        if attr_str[0] in ['-', '~', '#', '+']:
            attribute = ClassAttribute(AttributeModifier.from_string(attr_str[0]), attr_str[1:])
        else:
            attr_str = attr_str.strip()
            attribute = ClassAttribute(AttributeModifier.NONE, attr_str)

        if '(' in attr_str:
            self.methods.append(attribute)
        else:
            self.attributes.append(attribute)


class DiagramAnnotation(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon('@', ORANGE)


class DiagramEntity(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon('E', GREEN)


class DiagramEnum(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon('E', ORANGE)


class DiagramException(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon('X', RED)


class DiagramInterface(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)
        self.is_abstract = True

    def prepare_icon(self):
        return super().get_icon('I', PURPLE)


class DiagramMetaClass(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon('M', GRAY)


class DiagramProtocol(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon('P', LIGHT_GRAY)


class DiagramStereoType(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon('S', PINK)


class DiagramStruct(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon('S', LIGHT_GRAY)


class DiagramClassFactory:
    @staticmethod
    def make(name: str, class_type: ClassType | str = ClassType.CLASS):
        class_type = ClassType.from_string(class_type.lower()) if isinstance(class_type, str) else class_type

        if class_type == ClassType.CLASS:
            return DiagramClass(name)

        elif class_type == ClassType.ANNOTATION:
            return DiagramAnnotation(name)

        elif class_type == ClassType.ENTITY:
            return DiagramEntity(name)

        elif class_type == ClassType.ENUM:
            return DiagramEnum(name)

        elif class_type == ClassType.EXCEPTION:
            return DiagramException(name)

        elif class_type == class_type.INTERFACE:
            return DiagramInterface(name)

        elif class_type == class_type.META_CLASS:
            return DiagramMetaClass(name)

        elif class_type == class_type.PROTOCOL:
            return DiagramProtocol(name)

        elif class_type == class_type.STEREOTYPE:
            return DiagramStereoType(name)

        elif class_type == ClassType.STRUCT:
            return DiagramStruct(name)

        raise Exception('Undefined class type.')
