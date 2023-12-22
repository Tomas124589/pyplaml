from __future__ import annotations
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

        if string[0] in ['-', '~', '#', '+']:
            return ClassAttribute(AttributeModifier.from_string(string[0]), string[1:], is_method)
        else:
            attr_str = string.strip()
            return ClassAttribute(AttributeModifier.NONE, attr_str, is_method)
