import ply.yacc as yacc

from .class_attribute import ClassAttribute
from .class_type import ClassType
from .diagram import Diagram
from .diagram_class import DiagramClass, DiagramInterface, DiagramClassFactory
from .diagram_edge import DiagramEdge
from .diagram_note import DiagramNote
from .puml_lexer import PUMLexer
from .relation import Relation


class PUMLParser(object):

    def p_uml(self, p):
        """
        uml : STARTUML elements ENDUML
            | STARTUML strid elements ENDUML
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

    @staticmethod
    def p_strid(p):
        """
        strid   : IDENTIFIER
                | STRING
        """
        p[0] = p[1]

    def p_relation(self, p):
        """
        relation    : strid REL_LINE strid
                    | strid STRING REL_LINE strid
                    | strid REL_LINE STRING strid
                    | strid STRING REL_LINE STRING strid
        """
        left_class_name = p[1]
        right_class_name = p[len(p) - 1]
        line = p[2]
        l_text = ''
        r_text = ''

        _len = len(p)
        if _len > 4:
            if isinstance(p[2], str):
                if len(p) == 5:
                    l_text = p[2]
                    line = p[3]
                    r_text = ''
                else:
                    l_text = p[2]
                    line = p[3]
                    r_text = p[4]
            else:
                l_text = ''
                line = p[2]
                r_text = p[3]

        l_class = DiagramClass(left_class_name)
        r_class = DiagramClass(right_class_name)

        (left_rel, line, right_rel) = line

        source_rel = Relation.from_string(left_rel)
        target_rel = Relation.from_string(right_rel)

        is_left = source_rel != Relation.NONE
        is_right = target_rel != Relation.NONE

        if is_right:
            _dir = 1
        else:
            _dir = 0

        if _dir == 1:
            edge = DiagramEdge("." in line, l_class, r_class, source_rel, target_rel)

            edge.source_text = l_text
            edge.target_text = r_text

            l_class.add_edge(edge)
        else:
            edge = DiagramEdge("." in line, r_class, l_class, source_rel, target_rel)

            edge.source_text = r_text
            edge.target_text = l_text

            r_class.add_edge(edge)

        self.diagram.add(l_class, r_class, edge)

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

        edge.edge_text = text

        p[0] = (l_class, r_class, edge)

    def p_extends(self, p):
        """
        relation    : class EXTENDS strid
        """
        l_class: DiagramClass = p[1]
        if l_class.is_interface:
            r_class = DiagramInterface(p[3])
        else:
            r_class = DiagramClass(p[3])

        self.diagram.add(r_class)

        edge = DiagramEdge(False, l_class, r_class, source_rel=Relation.NONE, target_rel=Relation.EXTENSION)
        l_class.add_edge(edge)
        self.diagram.add(edge)

    def p_implements(self, p):
        """
        relation    : class IMPLEMENTS strid
        """
        l_class: DiagramClass = p[1]
        r_class = DiagramClassFactory.make(p[3], ClassType.INTERFACE)
        self.diagram.add(r_class)

        edge = DiagramEdge(True, l_class, r_class, Relation.NONE, Relation.EXTENSION)
        l_class.add_edge(edge)
        self.diagram.add(edge)

    def p_class(self, p):
        """
        class   : CLASS_DEF
                | CLASS_DEF GENERICS
        """
        (class_type, name, is_abstract) = p[1]
        c = DiagramClassFactory.make(name, class_type)
        c.set_abstract(is_abstract)

        if len(p) == 3:
            c.set_generics(p[2])

        self.diagram.add(c)

        p[0] = c

    @staticmethod
    def p_class_with_stereotype(p):
        """
        class   : class STEREOTYPE
        """
        p[0] = p[1].set_stereotype(p[2])

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
        p[0] = c.add_attributes([ClassAttribute.from_string(a) for a in p[2]])

    def p_class_alias(self, p):
        """
        class   : class AS IDENTIFIER
        """
        c: DiagramClass = p[1]

        self.diagram.objects.pop(str(c))
        c.alias = p[3]
        self.diagram.add(c)

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
        class_attr  : strid AFTERCOLON
        """
        c: DiagramClass = self.diagram[p[1]]
        p[0] = c.add_attributes([ClassAttribute.from_string(p[2])])

    def p_float_note(self, p):
        """
        note    : FLOAT_NOTE
                | FLOAT_NOTE NOTE_CONTENT
        """
        if len(p) == 2:
            note = DiagramNote(p[1][1], p[1][0])
        else:
            note = DiagramNote(p[1], "\n".join(p[2]))

        self.diagram.add(note)
        p[0] = note

    def p_line_note(self, p):
        """
        note    : LINE_NOTE
        """
        (pos, obj_name, text) = p[1]
        obj = self.diagram[obj_name]

        n = DiagramNote("{}-note-for-{}".format(pos, obj), text)
        e = DiagramEdge(False, n, obj)
        n.edges.append(e)

        self.diagram.add(n, e)

        p[0] = n

    def p_note(self, p):
        """
        note    : NOTE NOTE_CONTENT
        """
        (pos, obj_name) = p[1]
        obj = self.diagram[obj_name]
        text = "\n".join(p[2])

        n = DiagramNote("{}-note-for-{}".format(pos, obj), text)
        e = DiagramEdge(False, n, obj)
        n.edges.append(e)

        self.diagram.add(n, e)

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
        e = DiagramEdge(False, n, obj)
        n.edges.append(e)

        self.diagram.add(n, e)

        p[0] = n

    def p_remove(self, p):
        """
        command : REMOVE IDENTIFIER
        """
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
        self.diagram = Diagram()

    def parse(self, text) -> Diagram:
        return self.parser.parse(text)

    def parse_file(self, path):
        with open(path, "r") as file:
            text = file.read()

        return self.parse(text)
