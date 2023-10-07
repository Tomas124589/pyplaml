reserved = {
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
    "COLON",
] + list(reserved.values())


def t_LINE(t):
    r'[-\.]+'
    t.value = (int(t.value.count(".") + t.value.count("-")), "." in t.value)
    return t


def t_STRING(t):
    r'"(.*?)"'
    t.value = t.value.replace("\"", "")
    return t


def t_EXTENSION(t):
    r'<\||\|>'
    t.type = 'REL'
    t.value = 'EXTENSION'
    return t


def t_ASSOCIATION(t):
    r'<|>'
    t.type = 'REL'
    t.value = 'ASSOCIATION'
    return t


def t_AGGREGATION(t):
    r'o'
    t.type = 'REL'
    t.value = 'AGGREGATION'
    return t


def t_COMPOSITION(t):
    r'\*'
    t.type = 'REL'
    t.value = 'COMPOSITION'
    return t


def t_IDENTIFIER(t):
    r'@*[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_error(t):
    print("Illegal character: '{}'".format(t.value[0]))
    t.lexer.skip(1)


t_ignore = ' \n\t'
t_ignore_COMMENT = r"('.*)|(\/'(.|\s)*\'\/)"

t_COLON = r':'
