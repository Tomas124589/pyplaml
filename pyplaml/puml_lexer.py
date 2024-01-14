import re

import ply.lex as lex


# noinspection PyPep8Naming
class PUMLexer(object):
    states = (
        ("inbrackets", "exclusive"),
    )

    keywords = {
        "@startuml": "STARTUML",
        "@enduml": "ENDUML",
        "abstract": "ABSTRACT",
        "implements": "IMPLEMENTS",
        "extends": "EXTENDS",
        "as": "AS",
        "remove": "REMOVE",
        "hide": "HIDE",
        "show": "SHOW",
        "restore": "RESTORE",
        "note": "NOTE",
        "top": "TOP",
        "right": "RIGHT",
        "bottom": "BOTTOM",
        "left": "LEFT",
        "of": "OF",
        "end": "END",
    }

    tokens = [
                 "CLASS_DEF",
                 "IN_BRACKETS_LINES",
                 "REL_LINE",
                 "STRING",
                 "IDENTIFIER",
                 "AFTERCOLON",
                 "STEREOTYPE",
                 "GENERICS",
                 "TAG",
                 "MEMBER",
             ] + list(keywords.values())

    @staticmethod
    def t_STEREOTYPE(t):
        r"""<<(.+?)>>"""
        t.value = t.lexer.lexmatch.group(2).strip()
        return t

    @staticmethod
    def t_inbrackets(t):
        r"""\{"""
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.level = 1
        t.lexer.begin("inbrackets")

    @staticmethod
    def t_inbrackets_lbrace(t):
        r"""\{"""
        t.lexer.level += 1

    @staticmethod
    def t_inbrackets_rbrace(t):
        r"""\}"""
        t.lexer.level -= 1

        if t.lexer.level == 0:
            t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos - 1]
            t.lexer.lineno += t.value.count("\n")
            t.lexer.begin("INITIAL")
            t.type = "IN_BRACKETS_LINES"
            t.value = [val.strip() for val in t.value.splitlines() if val != ""]
            return t

    @staticmethod
    def t_REL_LINE(t):
        r"""(<\||<|o|\*|\#|x|\}|\+|\^)*(\-+|\.+)(\|>|>|o|\*|\#|x|\{|\+|\^)*"""
        left_type = t.lexer.lexmatch.group(5)
        line = t.lexer.lexmatch.group(6)
        right_type = t.lexer.lexmatch.group(7)

        t.value = (left_type, line, right_type)
        return t

    @staticmethod
    def t_GENERICS(t):
        r"""<(.+?)>"""
        t.value = t.lexer.lexmatch.group(9)
        return t

    @staticmethod
    def t_MEMBER(t):
        r"""(\w)::(.+)"""
        t.value = t.lexer.lexmatch.group(11), t.lexer.lexmatch.group(12)
        return t

    @staticmethod
    def t_STRING(t):
        r""""(.*?)\""""
        t.value = t.value.replace("\"", "")
        return t

    @staticmethod
    def t_CLASS_DEF(t):
        r"""\bclass\b|\bentity\b|\benum\b|\bexception\b|\binterface\b|\bmetaclass\b|\bprotocol\b|\bstereotype\b|\bstruct\b|\bannotation\b"""
        return t

    def t_IDENTIFIER(self, t):
        r"""@*\w+[()]*"""
        t.type = self.keywords.get(t.value.lower(), "IDENTIFIER")
        return t

    @staticmethod
    def t_TAG(t):
        r"""\$@*(\w+)"""
        t.value = t.value.strip()[1:]
        return t

    @staticmethod
    def t_AFTERCOLON(t):
        r""":.+"""
        t.value = t.value[1:].strip()
        return t

    @staticmethod
    def t_error(t):
        print("Illegal character: \"{}\"".format(t.value[0]))
        t.lexer.skip(1)

    @staticmethod
    def t_inbrackets_error(t):
        t.lexer.skip(1)

    t_ignore = " \n\t"
    t_ignore_COMMENT = r"('.*)|(\/'(.|\s)*\'\/)"

    t_inbrackets_ignore = " \t\n"

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, reflags=re.IGNORECASE, **kwargs)

    def test(self, text: str, output: bool = True):
        self.lexer.input(text)
        while output:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    def testFile(self, path: str, output: bool = True):
        with open(path, "r") as file:
            text = file.read()

        return self.test(text, output)
