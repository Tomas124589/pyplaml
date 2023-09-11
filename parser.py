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

    (first_nodes, others) = rels

    for n in first_nodes:
        d.addNode(n)

    if others is not None:
        while True:

            (first_nodes, others) = others
            for n in first_nodes:
                d.addNode(n)

            if others == None:
                break

    p[0] = d

def p_relations(p):
    """
    relations : relation
    relations : relation relations
    """
    length = len(p)
    if length == 2:
        p[0] = (p[1], None)
    elif length == 3:
        p[0] = (p[1], p[2])


def p_l_relation(p):
    """
    relation : IDENTIFIER REL LINE IDENTIFIER
    """
    # p[0] = (p[1], p[2], p[3], p[4])

    n1 = DiagramClass(p[1])
    n2 = DiagramClass(p[4])

    l = DiagramLine(p[2], n1, n2)
    p[0] = (n1, n2, l)


def p_r_relation(p):
    """
    relation : IDENTIFIER LINE REL IDENTIFIER
    """
    # p[0] = (p[1], p[3], p[2], p[4])

    n1 = DiagramClass(p[1])
    n2 = DiagramClass(p[4])
    l = DiagramLine(p[3], n1, n2)

    p[0] = (n1, n2, l)


def p_error(p):
    print("Parser syntax error:")
    print(p)
    print("======")

lexer = lex.lex(module=lexer_tokens, debug=False)

parser = yacc.yacc()