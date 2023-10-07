import ply.lex as lex
import ply.yacc as yacc

from pyPlantUML import *

import lexer_tokens
from lexer_tokens import tokens


def p_uml(p):
    """
    uml : START objects END
        | START IDENTIFIER objects END
        | START STRING objects END
    """

    name = ""
    objects = p[2]
    if len(p) == 5:
        name = p[2]
        objects = p[3]

    print("name: " + name)
    print("objects:")
    print(objects)

    p[0] = (p[1], p[2], p[3])


def p_objects(p):
    """
    objects : objects relation
            | relation
            | objects class
            | class
    """

    print("OBJS")
    print(p[1])
    if len(p) == 3:
        print(p[2])
    print("\n")

    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1], ())


def p_relation(p):
    """
    relation    : IDENTIFIER REL LINE REL IDENTIFIER
                | IDENTIFIER REL LINE IDENTIFIER
                | IDENTIFIER LINE REL IDENTIFIER
                | IDENTIFIER LINE IDENTIFIER
    """

    print("REL")
    print(*p)
    print("\n")

    p[0] = [*p]


def p_class(p):
    """
    class   : CLASS IDENTIFIER
            | CLASS STRING
            | ABS_CLASS CLASS IDENTIFIER
            | ABS_CLASS CLASS STRING
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
    """

    print("CLASS")
    print(*p)
    print("\n")

    p[0] = (p[1], p[2])


def p_error(p):
    print("Parser syntax error:")
    print(p)
    print("======")


lexer = lex.lex(module=lexer_tokens, debug=False)

parser = yacc.yacc()
