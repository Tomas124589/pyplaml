import ply.lex as lex
import ply.yacc as yacc

from pyPlantUML import *

import lexer_tokens
from lexer_tokens import tokens

def p_diagram(p):
    """
    diagram : START relations END
    diagram : START IDENTIFIER relations END
    diagram : START STRING relations END
    """
    length = len(p)

    if length == 4:

        d = Diagram("")
        rels = p[2]
    else:

        d = Diagram(p[2])
        rels = p[3]

    for i in rels:
        d.addObject(i)

    p[0] = d

def p_relations(p):
    """
    relations : relation
    relations : relation relations
    """
    length = len(p)
    if length == 2:
        p[0] = [p[1]]
    elif length == 3:
        if type(p[2]) is list:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1], p[2]]


def p_l_relation(p):
    """
    relation : IDENTIFIER REL LINE IDENTIFIER
    """

    n1 = DiagramClass(p[1])
    n2 = DiagramClass(p[4])
    l = DiagramLine(p[2], n1, n2)

    n1.addObject(n2)
    n1.addLine(l)

    p[0] = n1


def p_r_relation(p):
    """
    relation : IDENTIFIER LINE REL IDENTIFIER
    """

    n1 = DiagramClass(p[1])
    n2 = DiagramClass(p[4])
    l = DiagramLine(p[3], n1, n2)

    n1.addObject(n2)
    n1.addLine(l)

    p[0] = n1


def p_error(p):
    print("Parser syntax error:")
    print(p)
    print("======")

lexer = lex.lex(module=lexer_tokens, debug=False)

parser = yacc.yacc()