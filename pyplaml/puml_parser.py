import ply.yacc as yacc

from .diagram import Diagram
from .diagram_class import DiagramClass
from .diagram_edge import DiagramEdge
from .relation import Relation
from .puml_lexer import PUMLexer
from .class_attribute import ClassAttribute, AttributeModifier


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

        left_class_name = str(p[1])
        right_class_name = str(p[3])
        (edge, is_source_on_left) = p[2]
        edge: DiagramEdge

        l_class = DiagramClass(left_class_name, 'class').append_to_diagram(self.diagram)
        r_class = DiagramClass(right_class_name, 'class').append_to_diagram(self.diagram)

        if is_source_on_left:
            edge.source = l_class
            edge.target = r_class
            l_class.add_edge(edge)
        else:
            edge.source = r_class
            edge.target = l_class
            r_class.add_edge(edge)

        if len(p) == 5:
            edge.text = p[4]

        edge.append_to_diagram(self.diagram)

    def p_extends(self, p):
        """
        relation    : class EXTENDS IDENTIFIER
                    | class EXTENDS STRING
        """
        l_class: DiagramClass = p[1]
        r_class = DiagramClass(p[3], l_class.type).append_to_diagram(self.diagram)

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
        r_class = DiagramClass(p[3], 'interface').append_to_diagram(self.diagram)

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

        is_src_on_left = False

        if _len == 2:
            e = DiagramEdge("", p[1][1], p[1][0])
        elif _len == 3:
            if isinstance(p[1], str):
                e = DiagramEdge("", p[2][1], p[2][0])
                e.target_rel_type = Relation[p[1]]
            else:
                e = DiagramEdge("", p[1][1], p[1][0])
                e.target_rel_type = Relation[p[2]]
                is_src_on_left = True
        else:
            e = DiagramEdge("", p[2][0], p[2][1])
            e.source_rel_type = Relation[p[3]]
            e.target_rel_type = Relation[p[1]]

        p[0] = (e, is_src_on_left)

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
                (edge, is_src_on_left) = p[2]
                l_str = p[1]
                r_str = ""
            else:
                (edge, is_src_on_left) = p[1]
                l_str = ""
                r_str = p[2]
        else:
            (edge, is_src_on_left) = p[2]
            l_str = p[1]
            r_str = p[3]

        if is_src_on_left:
            edge.source_text = l_str
            edge.target_text = r_str
        else:
            edge.source_text = r_str
            edge.target_text = l_str

        p[0] = (edge, is_src_on_left)

    def p_class(self, p):
        """
        class   : CLASS_DEF IDENTIFIER
                | CLASS_DEF STRING
        """
        class_type = str(p[1]).lower()
        name = str(p[2])

        p[0] = DiagramClass(name, class_type).append_to_diagram(self.diagram)

    def p_abstract_class(self, p):
        """
        class           : ABSTRACT IDENTIFIER
                        | ABSTRACT STRING
                        | ABSTRACT class
        """
        if type(p[2]) is str:
            c = DiagramClass(p[2], 'abstract_class').append_to_diagram(self.diagram)
        else:
            c = self.diagram[p[2]]
            c.type = 'abstract_class'
        p[0] = c

    def p_class_attr(self, p):
        """
        class_attr  : IDENTIFIER AFTERCOLON
        class_attr  : STRING AFTERCOLON
        """

        o: DiagramClass = self.diagram.objects[p[1]]
        attr_str = str(p[2])
        is_method = '(' in attr_str

        if attr_str[0] in ['-', '~', '#', '+']:
            attribute = ClassAttribute(
                is_method, AttributeModifier.from_string(attr_str[0]), attr_str[1:])
        else:
            attr_str = attr_str.strip()
            attribute = ClassAttribute(
                is_method, AttributeModifier.NONE, attr_str)

        if is_method:
            o.methods.append(attribute)
        else:
            o.attributes.append(attribute)

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
