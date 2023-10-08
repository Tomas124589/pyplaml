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

    p[0] = (name, elements)


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
    line = p[3]
    rightClassName = str(p[4])

    if isinstance(p[2], tuple):
        relation = p[3]
        line = p[2]

    p[0] = (leftClassName, relation, line, rightClassName)


def p_simple_relation(p):
    """
    relation    : IDENTIFIER LINE IDENTIFIER
    """

    leftClassName = str(p[1])
    line = p[2]
    rightClassName = str(p[3])

    p[0] = (leftClassName, line, rightClassName)


def p_bi_relation(p):
    """
    relation    : IDENTIFIER REL LINE REL IDENTIFIER
    """

    leftClassName = str(p[1])
    leftRelation = p[2]
    line = p[3]
    rightRelation = p[4]
    rightClassName = str(p[5])

    p[0] = (leftClassName, leftRelation, line, rightRelation, rightClassName)


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

    p[0] = (classType, name)


def p_error(p):
    print("Parser syntax error:")
    print(p)
    print("======")


lexer = lex.lex(module=lexer_tokens, debug=False)

parser = yacc.yacc()
