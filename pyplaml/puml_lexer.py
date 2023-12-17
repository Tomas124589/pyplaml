import ply.lex as lex


# noinspection PyPep8Naming
class PUMLexer(object):
    keywords = {
        "@startuml": "START",
        "@enduml": "END",
        "abstract": "ABSTRACT",
        "implements": "IMPLEMENTS",
        "extends": "EXTENDS",
    }

    tokens = [
                 "CLASS_DEF",
                 "EXTENSION",
                 "ASSOCIATION",
                 "COMPOSITION",
                 "AGGREGATION",
                 "REL",
                 "STRING",
                 "IDENTIFIER",
                 "LINE",
                 "AFTERCOLON",
             ] + list(keywords.values())

    @staticmethod
    def t_LINE(t):
        r"""[-\.]+"""
        t.value = (int(t.value.count(".") + t.value.count("-")), "." in t.value)
        return t

    @staticmethod
    def t_STRING(t):
        r""""(.*?)\""""
        t.value = t.value.replace("\"", "")
        return t

    @staticmethod
    def t_EXTENSION(t):
        r"""<\||\|>|\^"""
        t.type = 'REL'
        t.value = 'EXTENSION'
        return t

    @staticmethod
    def t_ASSOCIATION(t):
        r"""<|>"""
        t.type = 'REL'
        t.value = 'ASSOCIATION'
        return t

    @staticmethod
    def t_AGGREGATION(t):
        r"""o"""
        t.type = 'REL'
        t.value = 'AGGREGATION'
        return t

    @staticmethod
    def t_COMPOSITION(t):
        r"""\*"""
        t.type = 'REL'
        t.value = 'COMPOSITION'
        return t

    @staticmethod
    def t_HASH(t):
        r"""\#"""
        t.type = 'REL'
        t.value = 'HASH'
        return t

    @staticmethod
    def t_CROSS(t):
        r"""x"""
        t.type = 'REL'
        t.value = 'CROSS'
        return t

    @staticmethod
    def t_CROW_FOOT(t):
        r"""\{|\}"""
        t.type = 'REL'
        t.value = 'CROW_FOOT'
        return t

    @staticmethod
    def t_NEST_CLASSIFIER(t):
        r"""\+"""
        t.type = 'REL'
        t.value = 'NEST_CLASSIFIER'
        return t

    @staticmethod
    def t_CLASS_DEF(t):
        r"""(?i)\bclass\b|\bentity\b|\benum\b|\bexception\b|\binterface\b|\bmetaclass\b|\bprotocol\b|\bstereotype\b|\bstruct\b|\bannotation\b"""
        return t

    def t_IDENTIFIER(self, t):
        r"""@*\w+[()]*"""
        t.type = self.keywords.get(t.value.lower(), 'IDENTIFIER')
        return t

    @staticmethod
    def t_AFTERCOLON(t):
        r""":.+"""
        t.value = t.value[1:].strip()
        return t

    @staticmethod
    def t_error(t):
        print("Illegal character: '{}'".format(t.value[0]))
        t.lexer.skip(1)

    t_ignore = ' \n\t'
    t_ignore_COMMENT = r"('.*)|(\/'(.|\s)*\'\/)"

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, text):
        self.lexer.input(text)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    def testFile(self, path):
        with open(path, 'r') as file:
            text = file.read()

        return self.test(text)
