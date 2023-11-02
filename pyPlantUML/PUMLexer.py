import ply.lex as lex


class PUMLexer(object):

    keywords = {
        "@startuml": "START",
        "@enduml": "END",
        "class": "CLASS",
        "Class": "CLASS",
        "abstract": "ABS_CLASS",
        "entity": "ENTITY",
        "enum": "ENUM",
        "exception": "EXCEPTION",
        "interface": "INTERFACE",
        "metaclass": "META_CLASS",
        "protocol": "PROTOCOL",
        "stereotype": "STEREOTYPE",
        "struct": "STRUCT",
    }

    tokens = [
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

    def t_LINE(self, t):
        r'[-\.]+'
        t.value = (int(t.value.count(".") + t.value.count("-")), "." in t.value)
        return t

    def t_STRING(self, t):
        r'"(.*?)"'
        t.value = t.value.replace("\"", "")
        return t

    def t_EXTENSION(self, t):
        r'<\||\|>|\^'
        t.type = 'REL'
        t.value = 'EXTENSION'
        return t

    def t_ASSOCIATION(self, t):
        r'<|>'
        t.type = 'REL'
        t.value = 'ASSOCIATION'
        return t

    def t_AGGREGATION(self, t):
        r'o'
        t.type = 'REL'
        t.value = 'AGGREGATION'
        return t

    def t_COMPOSITION(self, t):
        r'\*'
        t.type = 'REL'
        t.value = 'COMPOSITION'
        return t

    def t_HASH(self, t):
        r'\#'
        t.type = 'REL'
        t.value = 'HASH'
        return t

    def t_CROSS(self, t):
        r'x'
        t.type = 'REL'
        t.value = 'CROSS'
        return t

    def t_CROW_FOOT(self, t):
        r'\{|\}'
        t.type = 'REL'
        t.value = 'CROW_FOOT'
        return t

    def t_NEST_CLASSIFIER(self, t):
        r'\+'
        t.type = 'REL'
        t.value = 'NEST_CLASSIFIER'
        return t

    def t_IDENTIFIER(self, t):
        r'@*\w+[()]*'
        t.type = self.keywords.get(t.value, 'IDENTIFIER')
        return t

    def t_AFTERCOLON(self, t):
        r':.+'
        t.value = t.value[1:].strip()
        return t

    def t_error(self, t):
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
