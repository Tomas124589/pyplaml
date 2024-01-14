import ply.yacc as yacc

from .class_attribute import ClassAttribute
from .class_type import ClassType
from .diagram import Diagram
from .diagram_class import DiagramClass, DiagramClassFactory
from .diagram_edge import DiagramEdge
from .diagram_note import DiagramNote
from .puml_lexer import PUMLexer
from .relation import Relation


class PUMLParser(object):

    def p_uml(self, p):
        """
        uml : STARTUML elements ENDUML
            | STARTUML IDENTIFIER elements ENDUML
            | STARTUML STRING elements ENDUML
        """

        if len(p) == 5:
            self.diagram.name = p[2]

        p[0] = self.diagram

    def p_elements(self, p):
        """
        elements : elements relation
                | relation
                | elements class
                | class
                | elements class_attr
                | class_attr
                | elements command
                | command
                | elements note
                | note
                | elements skinparam
                | skinparam
        """

    def p_relation(self, p):
        """
        relation    : IDENTIFIER rel_line IDENTIFIER
                    | STRING rel_line STRING
                    | STRING rel_line IDENTIFIER
                    | IDENTIFIER rel_line STRING
        """
        edge: DiagramEdge = p[2]

        l_class = DiagramClass(p[1]).append_to_diagram(self.diagram)
        r_class = DiagramClass(p[3]).append_to_diagram(self.diagram)

        if edge.get_dir() == 1:
            edge.source = l_class
            edge.target = r_class
            l_class.edges.append(edge)
        else:
            edge.source = r_class
            edge.target = l_class
            r_class.edges.append(edge)

        edge.append_to_diagram(self.diagram)

        p[0] = (l_class, r_class, edge)

    @staticmethod
    def p_relation_aftercolon(p):
        """
        relation    : relation AFTERCOLON
        """
        (l_class, r_class, edge) = p[1]

        text = str(p[2]).strip()
        if text[0] == "<":
            edge.arrow_from_source = edge.get_dir() != 1
            text = text[1:]

        elif text[0] == ">":
            edge.arrow_from_source = edge.get_dir() == 1
            text = text[1:]

        edge.text = text

        p[0] = (l_class, r_class, edge)

    def p_extends(self, p):
        """
        relation    : class EXTENDS IDENTIFIER
                    | class EXTENDS STRING
        """
        l_class: DiagramClass = p[1]

        if l_class.is_interface:
            r_class = DiagramClassFactory.make(p[3], ClassType.INTERFACE).append_to_diagram(self.diagram)
        else:
            r_class = DiagramClass(p[3]).append_to_diagram(self.diagram)

        edge = DiagramEdge(False, 1)
        edge.source = l_class
        edge.source_rel_type = Relation.NONE
        edge.target = r_class
        edge.target_rel_type = Relation.EXTENSION

        l_class.edges.append(edge)
        edge.append_to_diagram(self.diagram)

    def p_implements(self, p):
        """
        relation    : class IMPLEMENTS IDENTIFIER
                    | class IMPLEMENTS STRING
        """
        l_class: DiagramClass = p[1]
        r_class = DiagramClassFactory.make(p[3], ClassType.INTERFACE).append_to_diagram(self.diagram)

        edge = DiagramEdge(True, 1)
        edge.source = l_class
        edge.source_rel_type = Relation.NONE
        edge.target = r_class
        edge.target_rel_type = Relation.EXTENSION

        l_class.edges.append(edge)
        edge.append_to_diagram(self.diagram)

    @staticmethod
    def p_rel_line(p):
        """
        rel_line    : REL_LINE
                    | STRING REL_LINE
                    | REL_LINE STRING
                    | STRING REL_LINE STRING
        """
        _len = len(p)
        if _len == 2:
            (left_type, line, right_type) = p[1]
            l_str = ""
            r_str = ""

        elif _len == 3:
            if isinstance(p[1], str):
                (left_type, line, right_type) = p[2]
                l_str = p[1]
                r_str = ""

            else:
                (left_type, line, right_type) = p[1]
                l_str = ""
                r_str = p[2]

        else:
            (left_type, line, right_type) = p[2]
            l_str = p[1]
            r_str = p[3]

        e = DiagramEdge("." in line, len(line))
        e.source_rel_type = Relation.from_string(left_type)
        e.target_rel_type = Relation.from_string(right_type)

        if e.get_dir() == 1:
            e.source_text = l_str
            e.target_text = r_str
        else:
            e.source_text = r_str
            e.target_text = l_str

        p[0] = e

    def p_class(self, p):
        """
        class   : CLASS_DEF
                | CLASS_DEF GENERICS
        """
        (class_type, name) = p[1]
        c = DiagramClassFactory.make(name, class_type).append_to_diagram(self.diagram)

        if len(p) == 3:
            c.generics = p[2]

        p[0] = c

    @staticmethod
    def p_class_with_stereotype(p):
        """
        class   : class STEREOTYPE
        """
        p[1].stereotype = p[2]

        p[0] = p[1]

    def p_abstract_class(self, p):
        """
        class           : ABSTRACT IDENTIFIER
                        | ABSTRACT STRING
                        | ABSTRACT class
        """
        if type(p[2]) is str:
            c = DiagramClass(p[2]).append_to_diagram(self.diagram)
        else:
            c = p[2]

        c.is_abstract = True
        p[0] = c

    def p_tagged_class(self, p):
        """
        class   : class tags
        """
        for t in p[2]:
            self.diagram.add_to_tagged(t, p[1])

        p[0] = p[1]

    @staticmethod
    def p_tags(p):
        """
        tags    : tags TAG
                | TAG
        """
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_class_with_body(self, p):
        """
        class   : class IN_BRACKETS_LINES
        """
        c: DiagramClass = self.diagram[p[1]]
        for l in p[2]:
            c.add_attribute(ClassAttribute.from_string(l))

        p[0] = c

    def p_class_alias(self, p):
        """
        class   : class AS IDENTIFIER
        """
        c: DiagramClass = p[1]

        self.diagram.objects.pop(str(c))
        c.alias = p[3]
        c.append_to_diagram(self.diagram)

        p[0] = p[1]

    @staticmethod
    def p_class_alias_str(p):
        """
        class   : class AS STRING
        """
        p[1].alias = p[1].name
        p[1].name = p[3]
        p[0] = p[1]

    def p_class_attr(self, p):
        """
        class_attr  : IDENTIFIER AFTERCOLON
                    | STRING AFTERCOLON
        """
        c: DiagramClass = self.diagram[p[1]]
        attr = ClassAttribute.from_string(p[2])
        c.add_attribute(attr)

    def p_float_note(self, p):
        """
        note    : FLOAT_NOTE
                | FLOAT_NOTE NOTE_CONTENT
        """
        if len(p) == 2:
            p[0] = DiagramNote(p[1][1], p[1][0]).append_to_diagram(self.diagram)
        else:
            p[0] = DiagramNote(p[1], "\n".join(p[2])).append_to_diagram(self.diagram)

    def p_line_note(self, p):
        """
        note    : LINE_NOTE
        """
        (pos, obj_name, text) = p[1]
        obj = self.diagram[obj_name]

        n = DiagramNote("{}-note-for-{}".format(pos, obj), text)
        e = DiagramEdge(False, 1)
        e.source = n
        e.target = obj
        n.edges.append(e)

        n.append_to_diagram(self.diagram)
        e.append_to_diagram(self.diagram)

        p[0] = n

    def p_note(self, p):
        """
        note    : NOTE NOTE_CONTENT
        """
        (pos, obj_name) = p[1]
        obj = self.diagram[obj_name]
        text = "\n".join(p[2])

        n = DiagramNote("{}-note-for-{}".format(pos, obj), text)
        e = DiagramEdge(False, 1)
        e.source = n
        e.target = obj
        n.edges.append(e)

        n.append_to_diagram(self.diagram)
        e.append_to_diagram(self.diagram)

        p[0] = n

    def p_note_last_object(self, p):
        """
        note    : NOTE_KW TOP AFTERCOLON
                | NOTE_KW RIGHT AFTERCOLON
                | NOTE_KW BOTTOM AFTERCOLON
                | NOTE_KW LEFT AFTERCOLON
        """
        obj = self.diagram.last_object
        pos = p[2]
        text = p[3]

        n = DiagramNote("{}-note-for-{}".format(pos, obj), text)
        e = DiagramEdge(False, 1)
        e.source = n
        e.target = obj
        n.edges.append(e)

        n.append_to_diagram(self.diagram)
        e.append_to_diagram(self.diagram)

        p[0] = n

    def p_remove(self, p):
        """
        command : REMOVE IDENTIFIER
        """
        print(p[2])
        if p[2][0] == "@":
            if p[2] == "@unlinked":
                self.diagram.remove_unlinked = True

            return

        self.diagram[p[2]].do_draw = False

    def p_remove_by_tag(self, p):
        """
        command : REMOVE TAG
        """
        self.diagram.remove_by_tag(p[2])

    def p_restore(self, p):
        """
        command : RESTORE IDENTIFIER
        """
        if p[2][0] == "@":
            if p[2] == "@unlinked":
                self.diagram.remove_unlinked = False

            return

        self.diagram[p[2]].do_draw = True

    def p_restore_by_tag(self, p):
        """
        command : RESTORE TAG
        """
        self.diagram.restore_by_tag(p[2])

    def p_hide(self, p):
        """
        command : HIDE IDENTIFIER
        """
        name = p[2]

        if name[0] == "@":
            if name == "@unlinked":
                self.diagram.hide_unlinked = True
        elif name == "circle":
            self.diagram.hide_icons = True
        else:
            self.diagram[name].is_hidden = True

    def p_hide_by_tag(self, p):
        """
        command : HIDE TAG
        """
        self.diagram.hide_by_tag(p[2])

    def p_show(self, p):
        """
        command : SHOW IDENTIFIER
        """
        name = p[2]

        if name[0] == "@":
            if name == "@unlinked":
                self.diagram.hide_unlinked = False
        elif name == "circle":
            self.diagram.hide_icons = False
        else:
            self.diagram[p[2]].is_hidden = False

    def p_show_by_tag(self, p):
        """
        command : SHOW TAG
        """
        self.diagram.show_by_tag(p[2])

    @staticmethod
    def p_skinparam(p):
        """
        skinparam   : SKINPARAM
        """
        skinparam = p[1].split(" ")[1::]

    @staticmethod
    def p_error(p):
        print("Parser syntax error:")
        print("\t", p)
        exit(1)

    def __init__(self, **kwargs):
        self.lexer = PUMLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)
        self.diagram = Diagram("")

    def parse(self, text) -> Diagram:
        return self.parser.parse(text)

    def parse_file(self, path):
        with open(path, "r") as file:
            text = file.read()

        return self.parse(text)
