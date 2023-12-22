import copy
import ply.yacc as yacc

from .diagram import Diagram
from .diagram_class import DiagramClass, DiagramClassFactory
from .diagram_edge import DiagramEdge
from .relation import Relation
from .puml_lexer import PUMLexer
from .class_type import ClassType


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
        """

    def p_relation(self, p):
        """
        relation    : IDENTIFIER rel_line IDENTIFIER
                    | IDENTIFIER rel_line IDENTIFIER AFTERCOLON
        """
        edge: DiagramEdge = p[2]

        l_class = DiagramClass(p[1]).append_to_diagram(self.diagram)
        r_class = DiagramClass(p[3]).append_to_diagram(self.diagram)

        edge_dir = edge.get_dir()
        if edge_dir == 1:
            edge.source = l_class
            edge.target = r_class
            l_class.add_edge(edge)
        else:
            edge.source = r_class
            edge.target = l_class
            r_class.add_edge(edge)

        if len(p) == 5:
            text = str(p[4]).strip()
            if text[0] == '<':
                edge.arrow_from_source = edge_dir != 1
                text = text[1:]

            elif text[0] == '>':
                edge.arrow_from_source = edge_dir == 1
                text = text[1:]

            edge.text = text

        edge.append_to_diagram(self.diagram)

    def p_extends(self, p):
        """
        relation    : class EXTENDS IDENTIFIER
                    | class EXTENDS STRING
        """
        l_class: DiagramClass = p[1]

        r_class = copy.deepcopy(l_class)
        r_class.name = p[3]
        r_class = r_class.append_to_diagram(self.diagram)

        edge = DiagramEdge(l_class.name, False, 1)
        edge.source = l_class
        edge.source_rel_type = Relation.NONE
        edge.target = r_class
        edge.target_rel_type = Relation.EXTENSION

        l_class.add_edge(edge)
        edge.append_to_diagram(self.diagram)

    def p_implements(self, p):
        """
        relation    : class IMPLEMENTS IDENTIFIER
                    | class IMPLEMENTS STRING
        """
        l_class: DiagramClass = p[1]
        r_class = DiagramClassFactory.make(p[3], ClassType.INTERFACE).append_to_diagram(self.diagram)

        edge = DiagramEdge(l_class.name, True, 1)
        edge.source = l_class
        edge.source_rel_type = Relation.NONE
        edge.target = r_class
        edge.target_rel_type = Relation.EXTENSION

        l_class.add_edge(edge)
        edge.append_to_diagram(self.diagram)

    @staticmethod
    def p_rel_line(p):
        """
        rel_line    : LINE
                    | REL LINE
                    | LINE REL
                    | REL LINE REL
        """
        _len = len(p)
        if _len == 2:
            e = DiagramEdge("", p[1][1], p[1][0])
        elif _len == 3:
            if isinstance(p[1], str):
                e = DiagramEdge("", p[2][1], p[2][0])
                e.source_rel_type = Relation[p[1]]
            else:
                e = DiagramEdge("", p[1][1], p[1][0])
                e.target_rel_type = Relation[p[2]]
        else:
            e = DiagramEdge("", p[2][0], p[2][1])
            e.source_rel_type = Relation[p[3]]
            e.target_rel_type = Relation[p[1]]

        p[0] = e

    @staticmethod
    def p_rel_line_named(p):
        """
        rel_line    : STRING rel_line STRING
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
        """
        p[0] = DiagramClassFactory.make(p[2], p[1]).append_to_diagram(self.diagram)

    def p_abstract_class(self, p):
        """
        class           : ABSTRACT IDENTIFIER
                        | ABSTRACT STRING
                        | ABSTRACT class
        """
        if type(p[2]) is str:
            c = DiagramClass(p[2]).append_to_diagram(self.diagram)
        else:
            c = self.diagram[p[2]]

        c.is_abstract = True
        p[0] = c

    def p_class_with_body(self, p):
        """
        class   : class class_body
        """
        c: DiagramClass = self.diagram[p[1]]
        for attr_str in p[2]:
            c.add_attribute(attr_str)

    @staticmethod
    def p_class_body(p):
        """
        class_body  : class_body TEXT_LINE
                    | TEXT_LINE
        """
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_class_attr(self, p):
        """
        class_attr  : IDENTIFIER AFTERCOLON
                    | STRING AFTERCOLON
        """
        c: DiagramClass = self.diagram[p[1]]
        c.add_attribute(p[2])

    @staticmethod
    def p_error(p):
        print("Parser syntax error:")
        print("\t", p)

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
