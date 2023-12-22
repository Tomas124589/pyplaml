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

    def __init__(self, modifier: AttributeModifier, text: str):
        self.modifier = modifier
        self.text = text
