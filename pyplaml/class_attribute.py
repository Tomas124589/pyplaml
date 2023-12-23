from __future__ import annotations

import re
from enum import Enum


class AttributeModifier(Enum):
    NONE = ""
    PRIVATE = "-"
    PACKAGE_PRIVATE = "~"
    PROTECTED = "#"
    PUBLIC = "+"

    @staticmethod
    def from_string(string: str) -> AttributeModifier:
        _mod = {member.value: member for member in AttributeModifier}.get(string)
        return AttributeModifier.NONE if _mod is None else _mod


class ClassAttribute:

    def __init__(self, modifier: AttributeModifier, text: str, is_method: bool):
        self.modifier = modifier
        self.text = text
        self.is_method = is_method
        self.is_abstract = False
        self.is_static = False

    @staticmethod
    def from_string(string: str) -> ClassAttribute:
        is_method = '(' in string

        sub = re.sub(r"(?i){field}", '', string)
        field_flag = string != sub
        string = sub

        sub = re.sub(r"(?i){method}", '', string)
        method_flag = string != sub
        string = sub

        sub = re.sub(r"(?i){static}", '', string)
        static_flag = string != sub
        string = sub

        sub = re.sub(r"(?i){abstract}", '', string)
        abstract_flag = string != sub
        string = sub

        string = string.strip()
        if string[0] in ['-', '~', '#', '+']:
            attr = ClassAttribute(AttributeModifier.from_string(string[0]), string[1:], is_method)
        else:
            attr_str = string.strip()
            attr = ClassAttribute(AttributeModifier.NONE, attr_str, is_method)

        if field_flag:
            attr.is_method = False
        elif method_flag:
            attr.is_method = True

        attr.is_static = static_flag
        attr.is_abstract = abstract_flag

        return attr
