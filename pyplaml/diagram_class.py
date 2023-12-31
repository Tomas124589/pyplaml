from manim import *

from .class_attribute import ClassAttribute
from .class_type import ClassType
from .diagram import Diagram
from .diagram_edge import DiagramEdge
from .diagram_object import DiagramObject


class DiagramClass(DiagramObject):

    def __init__(self, name: str):
        super().__init__(name)
        self.edges: List[DiagramEdge] = []
        self.attributes: List[ClassAttribute] = []
        self.methods: List[ClassAttribute] = []
        self.is_abstract = False
        self.is_interface = False
        self.stereotype = ""
        self.generics = ""

    def append_to_diagram(self, diagram: Diagram) -> DiagramObject:
        key = self.get_key()
        if key not in diagram.objects:
            diagram[key] = self
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
            diagram[key].edges += self.edges

        return diagram[key]

    def predraw(self):
        slant = ITALIC if self.is_abstract else NORMAL

        header = Rectangle(color=GRAY, fill_color=WHITE, fill_opacity=1)
        text = Text(self.name, color=BLACK, slant=slant)
        if self.stereotype:
            text = VGroup(
                Text("<<" + self.stereotype + ">>", color=BLACK).scale(0.6),
                text
            ).arrange(DOWN, buff=0.1)

        header.surround(text, buff=0.8)
        text_icon = (VGroup(self.prepare_icon(), text)
                     .arrange(RIGHT, buff=0.1))
        head_group = VGroup(header, text_icon)

        attr_body = Rectangle(color=GRAY, height=0.2, width=0.2, fill_color=WHITE, fill_opacity=1)
        attr_group = VGroup(attr_body)
        self.predraw_attributes(self.attributes, attr_body, attr_group)

        method_body = Rectangle(color=GRAY, height=0.2, width=0.2, fill_color=WHITE, fill_opacity=1)
        method_group = VGroup(method_body)
        self.predraw_attributes(self.methods, method_body, method_group)

        max_width = max(head_group.width, attr_group.width, method_group.width)

        header.stretch_to_fit_width(max_width)
        header.stretch_to_fit_height(text_icon.height + 0.2)

        attr_body.stretch_to_fit_width(max_width)
        method_body.stretch_to_fit_width(max_width)

        self.mobject = VGroup(
            head_group,
            attr_group,
            method_group
        ).stretch_to_fit_width(max_width).arrange(DOWN, buff=0)

        if self.generics:
            g_text = Text(self.generics, color=BLACK).scale(0.6)
            g_text.set_z_index(1)

            g_rect = DashedVMobject(Rectangle(color=BLACK, stroke_width=1), num_dashes=50)
            g_rect.stretch_to_fit_width(g_text.width + 0.1)
            g_rect.stretch_to_fit_height(g_text.height + 0.1)
            g_rect.set_z_index(1)

            g_back = Rectangle(fill_color=WHITE, fill_opacity=1)
            g_back.stretch_to_fit_width(g_rect.width - 0.05)
            g_back.stretch_to_fit_height(g_rect.height - 0.05)

            g_group = VGroup(g_rect, g_text, g_back)
            g_group.move_to(header.get_corner(UP + RIGHT) - (g_group.width / 2, 0, 0))

            head_group.add(g_group)

        return self.mobject

    @staticmethod
    def predraw_attributes(attributes: List[ClassAttribute], body: Rectangle, group: VGroup):
        if len(attributes) != 0:
            methods = VGroup()
            for a in attributes:
                slant = ITALIC if a.is_abstract else NORMAL
                text = Text(a.text, color=BLACK, slant=slant)

                if a.is_static:
                    text = VGroup(text, Underline(text, color=BLACK, buff=0, stroke_width=1))

                methods.add(VGroup(
                    Text(a.modifier.value, color=BLACK),
                    text
                ).arrange(RIGHT, buff=0.1).scale(0.75))

            methods.arrange(DOWN, buff=0.1)
            group.add(methods)
            body.surround(methods, buff=0.2)
            body.stretch_to_fit_height(methods.height + 0.1)

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

    def add_attribute(self, attr: ClassAttribute):
        if attr.is_method:
            self.methods.append(attr)
        else:
            self.attributes.append(attr)


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
        self.is_interface = True

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
