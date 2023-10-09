import ply.lex as lex
import ply.yacc as yacc

from pyPlantUML import *

import lexer_tokens
from lexer_tokens import tokens


def p_uml(p):
    """
    uml : START elements END
        | START IDENTIFIER elements END
        | START STRING elements END
    """

    name = ""
    elements = p[2]
    if len(p) == 5:
        name = p[2]
        elements = p[3]

    elementsFlattened = [e for tuple in elements for e in tuple]

    diagram = Diagram(name)

    for e in elementsFlattened:
        diagram.addObject(e)

    p[0] = diagram


def p_elements(p):
    """
    elements : elements relation
            | relation
            | elements class
            | class
    """

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_relation(p):
    """
    relation    : IDENTIFIER REL LINE IDENTIFIER
                | IDENTIFIER LINE REL IDENTIFIER
    """

    leftClassName = str(p[1])
    relation = p[2]
    lineData = p[3]
    rightClassName = str(p[4])

    if isinstance(p[2], tuple):
        relation = p[3]
        lineData = p[2]

    leftClass = DiagramClass(leftClassName, 'class')
    rightClass = DiagramClass(rightClassName, 'class')
    line = DiagramLine(
        leftClassName + "-" + relation + "-" + rightClassName,
        leftClass,
        lineData[1],
        lineData[0],
        "none",
        relation
    )

    rightClass.addLine(line)

    p[0] = (leftClass, rightClass)


def p_simple_relation(p):
    """
    relation    : IDENTIFIER LINE IDENTIFIER
    """

    leftClassName = str(p[1])
    lineData = p[2]
    rightClassName = str(p[3])

    leftClass = DiagramClass(leftClassName, 'class')
    rightClass = DiagramClass(rightClassName, 'class')

    line = DiagramLine(
        leftClassName + "-" + rightClassName,
        leftClass,
        lineData[1],
        lineData[0],
        "none",
        "none"
    )

    rightClass.addLine(leftClass)

    p[0] = (leftClass, rightClass)


def p_bi_relation(p):
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
    line = DiagramLine(
        leftClassName + "-" + leftRelation + "-" + rightRelation + "-" + rightClassName,
        leftClass,
        lineData[1],
        lineData[0],
        leftRelation,
        rightRelation
    )

    rightClass.addLine(line)

    p[0] = (leftClass, rightClass)


def p_class(p):
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

    p[0] = classObj


def p_error(p):
    print("Parser syntax error:")
    print(p)
    print("======")


lexer = lex.lex(module=lexer_tokens, debug=False)

parser = yacc.yacc()
