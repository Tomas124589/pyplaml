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

    def __init__(
            self,
            text: str,
            is_method: bool = False,
            modifier: AttributeModifier = AttributeModifier.PUBLIC,
            is_abstract: bool = False,
            is_static: bool = False
    ):
        self.text = text
        self.is_method = is_method
        self.modifier = modifier
        self.is_abstract = is_abstract
        self.is_static = is_static

    @staticmethod
    def from_string(string: str) -> ClassAttribute:
        sub = re.sub(r"(?i){field}", "", string)
        is_field = string != sub
        string = sub

        sub = re.sub(r"(?i){method}", "", string)
        is_method = (string != sub or "(" in string) and not is_field
        string = sub

        sub = re.sub(r"(?i){static}", "", string)
        is_static = string != sub
        string = sub

        sub = re.sub(r"(?i){abstract}", "", string)
        is_abstract = string != sub
        string = sub

        string = string.strip()

        if string[0] in ["-", "~", "#", "+"]:
            text = string[1:]
            modifier = AttributeModifier.from_string(string[0])
        else:
            text = string
            modifier = AttributeModifier.NONE

        return ClassAttribute(text, is_method, modifier, is_abstract, is_static)
