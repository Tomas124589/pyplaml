import re

import ply.lex as lex


# noinspection PyPep8Naming
class PUMLexer(object):
    states = (
        ("inbrackets", "exclusive"),
        ("NOTE", "exclusive"),
    )

    keywords = {
        "@startuml": "STARTUML",
        "@enduml": "ENDUML",
        "implements": "IMPLEMENTS",
        "extends": "EXTENDS",
        "as": "AS",
        "remove": "REMOVE",
        "hide": "HIDE",
        "show": "SHOW",
        "restore": "RESTORE",
        "note": "NOTE_KW",
        "top": "TOP",
        "right": "RIGHT",
        "bottom": "BOTTOM",
        "left": "LEFT",
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
                 "SKINPARAM",
                 "LINE_NOTE",
                 "FLOAT_NOTE",
                 "NOTE_CONTENT",
                 "NOTE"
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
    def t_LINE_NOTE(t):
        r"""note\s+(?:(top|right|bottom|left) of)\s+("[^"]*"|\w+)(?:\s*:\s*(.*))"""
        pos = t.lexer.lexmatch.group(5)
        obj_name = t.lexer.lexmatch.group(6)
        text = t.lexer.lexmatch.group(7)

        t.value = (pos, obj_name, text)
        return t

    @staticmethod
    def t_NOTE(t):
        r"""note\s+(?:(top|right|bottom|left) of)\s+("[^"]*"|\w+)"""
        t.lexer.begin("NOTE")
        t.lexer.note_start = t.lexer.lexpos

        pos = t.lexer.lexmatch.group(9)
        obj_name = t.lexer.lexmatch.group(10)
        t.value = (pos, obj_name)
        return t

    @staticmethod
    def t_FLOAT_NOTE(t):
        r"""note\s+"([^"]*)"\s+AS\s+(.*)"""
        text = t.lexer.lexmatch.group(12)
        alias = t.lexer.lexmatch.group(13)

        t.value = (text, alias)
        return t

    @staticmethod
    def t_FLOAT_NOTE_MULTILINE(t):
        r"""note\s+AS\s+(.*)"""
        t.lexer.begin("NOTE")
        t.lexer.note_start = t.lexer.lexpos

        t.type = "FLOAT_NOTE"
        t.value = t.lexer.lexmatch.group(15)
        return t

    @staticmethod
    def t_NOTE_CONTENT(t):
        r"""end note"""
        t.lexer.begin("INITIAL")
        t.lexer.lineno += t.value.count("\n")

        t.type = "NOTE_CONTENT"

        t.value = t.lexer.lexdata[t.lexer.note_start:t.lexer.lexpos]
        t.value = [val.strip() for val in t.value.splitlines() if val != ""][:-1]
        return t

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
        left_type = t.lexer.lexmatch.group(17)
        line = t.lexer.lexmatch.group(18)
        right_type = t.lexer.lexmatch.group(19)

        t.value = (left_type, line, right_type)
        return t

    @staticmethod
    def t_GENERICS(t):
        r"""<(.+?)>"""
        t.value = t.lexer.lexmatch.group(21)
        return t

    @staticmethod
    def t_MEMBER(t):
        r"""(\w)::(.+)"""
        t.value = t.lexer.lexmatch.group(23), t.lexer.lexmatch.group(24)
        return t

    @staticmethod
    def t_STRING(t):
        r""""(.*?)\""""
        t.value = t.value.replace("\"", "")
        return t

    @staticmethod
    def t_CLASS_DEF(t):
        r"""(?:(abstract)\s+)?(class|abstract|entity|enum|exception|interface|metaclass|protocol|stereotype|struct|annotation|object)\s+("[^"]*"|\w+)"""
        is_abstract = t.lexer.lexmatch.group(28) == 'abstract'
        class_type = t.lexer.lexmatch.group(29)
        name = t.lexer.lexmatch.group(30).replace("\"", "")

        if class_type == 'abstract':
            is_abstract = True
            class_type = 'class'

        t.value = (class_type, name, is_abstract)
        return t

    @staticmethod
    def t_SKINPARAM(t):
        r"""skinparam\s+(\w+)\s+(\w+)?"""
        target = t.lexer.lexmatch.group(32)
        value = t.lexer.lexmatch.group(33)

        t.value = (target, value)
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

    @staticmethod
    def t_NOTE_error(t):
        t.lexer.skip(1)

    t_ignore = " \n\t"
    t_ignore_COMMENT = r"('.*)|(\/'(.|\s)*\'\/)"

    t_inbrackets_ignore = " \t\n"
    t_NOTE_ignore = " \t\n"

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
