import ply.yacc as yacc

from .class_attribute import ClassAttribute
from .class_type import ClassType
from .diagram import Diagram
from .diagram_class import DiagramClass, DiagramClassFactory
from .diagram_edge import DiagramEdge
from .puml_lexer import PUMLexer
from .relation import Relation


class PUMLParser(object):

    def p_uml(self, p):
        """
        uml : START elements END
            | START IDENTIFIER elements END
            | START STRING elements END
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
        """

    def p_relation(self, p):
        """
        relation    : IDENTIFIER rel_line IDENTIFIER
                    | IDENTIFIER rel_line_named IDENTIFIER
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
        if text[0] == '<':
            edge.arrow_from_source = edge.get_dir() != 1
            text = text[1:]

        elif text[0] == '>':
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
        """
        (left_type, line, right_type) = p[1]

        is_dashed = "." in line
        line_length = len(line)

        e = DiagramEdge(is_dashed, line_length)
        e.source_rel_type = Relation.from_string(left_type)
        e.target_rel_type = Relation.from_string(right_type)

        p[0] = e

    @staticmethod
    def p_rel_line_named(p):
        """
        rel_line_named  : STRING rel_line STRING
                        | rel_line STRING
                        | STRING rel_line
        """
        _len = len(p)
        if _len == 3:
            if isinstance(p[1], str):
                edge = p[2]
                l_str = p[1]
                r_str = ""
            else:
                edge = p[1]
                l_str = ""
                r_str = p[2]
        else:
            edge = p[2]
            l_str = p[1]
            r_str = p[3]

        if edge.get_dir() == 1:
            edge.source_text = l_str
            edge.target_text = r_str
        else:
            edge.source_text = r_str
            edge.target_text = l_str

        p[0] = edge

    def p_class(self, p):
        """
        class   : CLASS_DEF IDENTIFIER
                | CLASS_DEF STRING
                | CLASS_DEF IDENTIFIER GENERICS
                | CLASS_DEF STRING GENERICS
        """
        c = DiagramClassFactory.make(p[2], p[1]).append_to_diagram(self.diagram)

        if len(p) == 4:
            c.generics = p[3]

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

    def p_remove(self, p):
        """
        command : REMOVE IDENTIFIER
        """
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
        self.diagram[p[2]].is_hidden = True

    def p_hide_by_tag(self, p):
        """
        command : HIDE TAG
        """
        self.diagram.hide_by_tag(p[2])

    def p_show(self, p):
        """
        command : SHOW IDENTIFIER
        """
        self.diagram[p[2]].is_hidden = False

    def p_show_by_tag(self, p):
        """
        command : SHOW TAG
        """
        self.diagram.show_by_tag(p[2])

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
        with open(path, 'r') as file:
            text = file.read()

        return self.parse(text)
