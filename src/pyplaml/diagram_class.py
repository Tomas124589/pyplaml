from __future__ import annotations

from manim import *

from .class_attribute import ClassAttribute
from .class_type import ClassType
from .diagram import Diagram
from .diagram_edge import DiagramEdge
from .diagram_object import DiagramObject


class DiagramClass(DiagramObject):

    def __init__(self,
                 name: str,
                 edges: List[DiagramEdge] = None,
                 attributes: List[ClassAttribute] = None,
                 stereotype: str = "",
                 generics: str = "",
                 **kwargs):
        super().__init__(name, **kwargs)
        if edges is None:
            edges: List[DiagramEdge] = []
        self.edges = edges

        if attributes is None:
            attributes: List[ClassAttribute] = []
        self.__attributes = attributes

        self.__stereotype = stereotype
        self.__generics = generics

        self.__show_icon = True
        self.__is_abstract = False
        self.is_interface = False

        self.__mg_header = VGroup()
        self.__mo_title = Text
        self.__mg_attributes = VGroup()
        self.__mg_methods = VGroup()

        self.redraw()

    def append_to_diagram(self, diagram: Diagram) -> DiagramClass:
        key = self.get_key()
        exists = key in diagram.objects
        if not exists:
            diagram[key] = self
            for edge in self.edges:
                if edge.target.name not in diagram.objects:
                    diagram.add(edge.target)
                edge.target = diagram[edge.target.name]
        else:
            for edge in self.edges:
                if edge.target.name not in diagram.objects:
                    diagram.add(edge.target)
                edge.target = diagram[edge.target.name]
            diagram[key].edges += self.edges

        return diagram[key]

    def add_edge(self, edge: DiagramEdge) -> DiagramEdge:
        self.edges.append(edge)
        return edge

    def get_edges(self) -> List[DiagramEdge]:
        return self.edges

    def get_edge_to(self, target: DiagramObject) -> DiagramEdge | None:
        for e in self.edges:
            if e.target == target:
                return e
        return None

    def add_attributes(self, attributes: List[ClassAttribute]) -> DiagramClass:
        for a in attributes:
            self.__attributes.append(a)
        self.redraw()
        return self

    def set_stereotype(self, stereotype: str) -> DiagramClass:
        self.__stereotype = stereotype
        self.redraw()
        return self

    def set_abstract(self, is_abstract: bool):
        self.__is_abstract = is_abstract
        self.redraw()

    def set_generics(self, generics: str):
        self.__generics = generics
        self.redraw()

    def set_show_icon(self, show_icon: bool):
        self.__show_icon = show_icon
        self.redraw()

    def draw(self):
        header = self.__prepare_header()
        attr_body = self.__prepare_attributes_body()
        method_body = self.__prepare_methods_body()

        max_width = max(self.__mg_header.width, self.__mg_attributes.width, self.__mg_methods.width)

        header.stretch_to_fit_width(max_width)
        attr_body.stretch_to_fit_width(max_width)
        method_body.stretch_to_fit_width(max_width)

        mgroup = VGroup(
            self.__mg_header,
            self.__mg_attributes,
            self.__mg_methods
        ).arrange(DOWN, buff=0)

        if self.__generics:
            self.__mg_header.add(self.__prepare_generics())

        if self.notes:
            self.__prepare_notes(mgroup)

        return mgroup

    def __prepare_notes(self, parent: VGroup):
        note_groups = VGroup()
        for _dir, notes in self.notes.items():
            vect = _dir.get_manim_vect_dir()
            note_groups.add(
                VGroup(*notes)
                .arrange(-vect)
                .next_to(parent, vect)
            )

        parent.add(note_groups)

    def redraw(self):
        if self.do_draw:
            self.become(self.draw(), match_center=True)

    def __prepare_header(self):
        mo_title = self.__prepare_title()

        header = Rectangle(color=GRAY, fill_color=WHITE, fill_opacity=1)
        header.stretch_to_fit_width(mo_title.width + 0.5)
        header.stretch_to_fit_height(mo_title.height + 0.2)

        self.__mg_header = VGroup(header, mo_title)

        return header

    def __prepare_title(self):
        self.__mo_title = Text(self.name, color=BLACK, slant=ITALIC if self.__is_abstract else NORMAL)
        if self.__stereotype:
            text_group = VGroup(
                Text("<<" + self.__stereotype + ">>", color=BLACK).scale(0.6),
                self.__mo_title
            ).arrange(DOWN, buff=0.1)
        else:
            text_group = self.__mo_title

        return VGroup(
            self.prepare_icon() if self.__show_icon else VGroup(),
            text_group).arrange(RIGHT, buff=0.1)

    def __prepare_attributes_body(self):
        attributes = self.__prepare_attributes([a for a in self.__attributes if not a.is_method])
        border = Rectangle(color=GRAY, height=attributes.height + 0.1, width=0.2, fill_color=WHITE, fill_opacity=1)
        self.__mg_attributes = VGroup(border, attributes)
        border.stretch_to_fit_width(self.__mg_attributes.width + 0.1)

        return border

    def __prepare_methods_body(self):
        methods = self.__prepare_attributes([a for a in self.__attributes if a.is_method])
        border = Rectangle(color=GRAY, height=methods.height + 0.1, width=0.2, fill_color=WHITE, fill_opacity=1)
        self.__mg_methods = VGroup(border, methods)
        border.stretch_to_fit_width(self.__mg_methods.width + 0.1)

        return border

    def __prepare_generics(self):
        g_text = Text(self.__generics, color=BLACK).scale(0.6)

        g_rect = DashedVMobject(Rectangle(color=BLACK, stroke_width=1), num_dashes=50)
        g_rect.stretch_to_fit_width(g_text.width + 0.1)
        g_rect.stretch_to_fit_height(g_text.height + 0.1)

        g_back = Rectangle(fill_color=WHITE, fill_opacity=1)
        g_back.stretch_to_fit_width(g_rect.width - 0.05)
        g_back.stretch_to_fit_height(g_rect.height - 0.05)

        g_group = VGroup(g_back, g_rect, g_text)
        g_group.move_to(self.__mg_header.get_corner(UP + RIGHT) - (g_group.width / 2, 0, 0))

        return g_group

    @staticmethod
    def __prepare_attributes(attributes: List[ClassAttribute]):
        attr_group = VGroup()
        for a in attributes:
            text = Text(a.text, color=BLACK, slant=ITALIC if a.is_abstract else NORMAL)

            if a.is_static:
                text = VGroup(text, Underline(text, color=BLACK, buff=0, stroke_width=1))

            attr_group.add(VGroup(
                Text(a.modifier.value, color=BLACK),
                text
            ).arrange(RIGHT, buff=0.1).scale(0.75))

        return attr_group.arrange(DOWN, buff=0.1)

    @staticmethod
    def get_icon(text: str, colour) -> VMobject:
        c = Circle(color=BLACK, fill_color=colour, stroke_width=2, fill_opacity=1)
        t = Text(text, color=BLACK)
        c.surround(t, buffer_factor=1.6)
        return VGroup(c, t)

    def prepare_icon(self):
        return self.get_icon("A" if self.__is_abstract else "C", TEAL if self.__is_abstract else GREEN)


class DiagramAnnotation(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon("@", ORANGE)


class DiagramEntity(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon("E", GREEN)


class DiagramEnum(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon("E", ORANGE)


class DiagramException(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon("X", RED)


class DiagramInterface(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)
        self.is_abstract = True
        self.is_interface = True

    def prepare_icon(self):
        return super().get_icon("I", PURPLE)


class DiagramMetaClass(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon("M", GRAY)


class DiagramProtocol(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon("P", LIGHT_GRAY)


class DiagramStereoType(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon("S", PINK)


class DiagramStruct(DiagramClass):
    def __init__(self, name: str):
        super().__init__(name)

    def prepare_icon(self):
        return super().get_icon("S", LIGHT_GRAY)


class DiagramPlainObject(DiagramClass):
    def __init__(self, name):
        super().__init__(name)
        self.show_icon = False

    def prepare_icon(self):
        return VGroup()


class DiagramClassFactory:
    @staticmethod
    def make(name: str, class_type: ClassType | str = ClassType.CLASS):
        class_type = ClassType.from_string(class_type) if isinstance(class_type, str) else class_type

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

        elif class_type == class_type.METACLASS:
            return DiagramMetaClass(name)

        elif class_type == class_type.PROTOCOL:
            return DiagramProtocol(name)

        elif class_type == class_type.STEREOTYPE:
            return DiagramStereoType(name)

        elif class_type == ClassType.STRUCT:
            return DiagramStruct(name)

        elif class_type == ClassType.OBJECT:
            return DiagramPlainObject(name)

        raise Exception("Undefined class type.")
