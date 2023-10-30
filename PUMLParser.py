import ply.yacc as yacc

from PUMLexer import PUMLexer

from pyPlantUML import *


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
        """

    def p_left_relation(self, p):
        """
        relation    : IDENTIFIER REL LINE IDENTIFIER
        """

        leftClassName = str(p[1])
        relation = p[2]
        lineData = p[3]
        rightClassName = str(p[4])

        leftClass = DiagramClass(leftClassName, 'class')
        rightClass = DiagramClass(rightClassName, 'class')
        line = DiagramEdge(
            leftClassName + "-" + relation + "-" + rightClassName,
            leftClass,
            lineData[1],
            lineData[0],
            Relation["NONE"],
            Relation[relation],
        )

        rightClass.addEdge(line)

        self.diagram.addObject(leftClass)
        self.diagram.addObject(rightClass)

    def p_right_relation(self, p):
        """
        relation    : IDENTIFIER LINE REL IDENTIFIER
        """

        leftClassName = str(p[1])
        lineData = p[2]
        relation = p[3]
        rightClassName = str(p[4])

        leftClass = DiagramClass(leftClassName, 'class')
        rightClass = DiagramClass(rightClassName, 'class')
        line = DiagramEdge(
            leftClassName + "-" + relation + "-" + rightClassName,
            rightClass,
            lineData[1],
            lineData[0],
            Relation["NONE"],
            Relation[relation],
        )

        leftClass.addEdge(line)

        self.diagram.addObject(leftClass)
        self.diagram.addObject(rightClass)

    def p_simple_relation(self, p):
        """
        relation    : IDENTIFIER LINE IDENTIFIER
        """

        leftClassName = str(p[1])
        lineData = p[2]
        rightClassName = str(p[3])

        leftClass = DiagramClass(leftClassName, 'class')
        rightClass = DiagramClass(rightClassName, 'class')

        line = DiagramEdge(
            leftClassName + "-" + rightClassName,
            leftClass,
            lineData[1],
            lineData[0],
            Relation["NONE"],
            Relation["NONE"],
        )

        rightClass.addEdge(leftClass)

        self.diagram.addObject(leftClass)
        self.diagram.addObject(rightClass)

    def p_bi_relation(self, p):
        """
        relation    : IDENTIFIER REL LINE REL IDENTIFIER
        """

        leftClassName = str(p[1])
        leftRelation = p[2]
        lineData = p[3]
        rightRelation = p[4]
        rightClassName = str(p[5])

        leftClass = DiagramClass(leftClassName, 'class')
        rightClass = DiagramClass(rightClassName, 'class')
        line = DiagramEdge(
            leftClassName + "-" + leftRelation + "-" + rightRelation + "-" + rightClassName,
            leftClass,
            lineData[1],
            lineData[0],
            Relation[leftRelation],
            Relation[rightRelation],
        )

        rightClass.addEdge(line)

        self.diagram.addObject(leftClass)
        self.diagram.addObject(rightClass)

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

        classType = str(p[1]).lower()
        name = str(p[2])
        if classType == "abstract":
            classType = "abstract_class"
            name = str(p[3])

        classObj = DiagramClass(name, classType)

        self.diagram.addObject(classObj)

    def p_error(self, p):
        print("Parser syntax error:")
        print("\t", p)

    def __init__(self, **kwargs):
        self.lexer = PUMLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)
        self.diagram = Diagram("")

    def parse(self, text):
        return self.parser.parse(text)

    def parseFile(self, path):
        with open(path, 'r') as file:
            text = file.read()

        return self.parse(text)
