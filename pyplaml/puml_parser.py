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

    def p_left_relation(self, p):
        """
        relation    : IDENTIFIER REL LINE IDENTIFIER
        """

        left_class_name = str(p[1])
        relation = p[2]
        line_data = p[3]
        right_class_name = str(p[4])

        left_class = DiagramClass(left_class_name, 'class')
        right_class = DiagramClass(right_class_name, 'class')
        line = DiagramEdge(
            left_class_name + "-" + relation + "-" + right_class_name,
            right_class,
            left_class,
            line_data[1],
            line_data[0],
            Relation["NONE"],
            Relation[relation],
        )

        right_class.add_edge(line)

        self.diagram.add_object(left_class)
        self.diagram.add_object(right_class)

    def p_right_relation(self, p):
        """
        relation    : IDENTIFIER LINE REL IDENTIFIER
        """

        left_class_name = str(p[1])
        line_data = p[2]
        relation = p[3]
        right_class_name = str(p[4])

        left_class = DiagramClass(left_class_name, 'class')
        right_class = DiagramClass(right_class_name, 'class')
        line = DiagramEdge(
            left_class_name + "-" + relation + "-" + right_class_name,
            left_class,
            right_class,
            line_data[1],
            line_data[0],
            Relation["NONE"],
            Relation[relation],
        )

        left_class.add_edge(line)

        self.diagram.add_object(left_class)
        self.diagram.add_object(right_class)

    def p_simple_relation(self, p):
        """
        relation    : IDENTIFIER LINE IDENTIFIER
        """

        left_class_name = str(p[1])
        line_data = p[2]
        right_class_name = str(p[3])

        left_class = DiagramClass(left_class_name, 'class')
        right_class = DiagramClass(right_class_name, 'class')

        line = DiagramEdge(
            left_class_name + "-" + right_class_name,
            right_class,
            left_class,
            line_data[1],
            line_data[0],
            Relation["NONE"],
            Relation["NONE"],
        )

        right_class.add_edge(line)

        self.diagram.add_object(left_class)
        self.diagram.add_object(right_class)

    def p_bi_relation(self, p):
        """
        relation    : IDENTIFIER REL LINE REL IDENTIFIER
        """

        left_class_name = str(p[1])
        left_relation = p[2]
        line_data = p[3]
        right_relation = p[4]
        right_class_name = str(p[5])

        left_class = DiagramClass(left_class_name, 'class')
        right_class = DiagramClass(right_class_name, 'class')
        line = DiagramEdge(
            left_class_name + "-" + left_relation + "-" + right_relation + "-" + right_class_name,
            right_class,
            left_class,
            line_data[1],
            line_data[0],
            Relation[left_relation],
            Relation[right_relation],
        )

        right_class.add_edge(line)

        self.diagram.add_object(left_class)
        self.diagram.add_object(right_class)

    def p_class(self, p):
        """
        class   : CLASS IDENTIFIER
                | CLASS STRING
                | ENTITY IDENTIFIER
                | ENTITY STRING
                | ENUM IDENTIFIER
                | ENUM STRING
                | EXCEPTION IDENTIFIER
                | EXCEPTION STRING
                | INTERFACE IDENTIFIER
                | INTERFACE STRING
                | META_CLASS IDENTIFIER
                | META_CLASS STRING
                | PROTOCOL IDENTIFIER
                | PROTOCOL STRING
                | STEREOTYPE IDENTIFIER
                | STEREOTYPE STRING
                | STRUCT IDENTIFIER
                | STRUCT STRING
                | ABS_CLASS CLASS IDENTIFIER
                | ABS_CLASS CLASS STRING
        """

        class_type = str(p[1]).lower()
        name = str(p[2])
        if class_type == "abstract":
            class_type = "abstract_class"
            name = str(p[3])

        class_obj = DiagramClass(name, class_type)

        self.diagram.add_object(class_obj)

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
