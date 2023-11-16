from enum import Enum


class AttributeModifier(Enum):
    NONE = ""
    PRIVATE = "-"
    PACKAGE_PRIVATE = "~"
    PROTECTED = "#"
    PUBLIC = "+"

    @staticmethod
    def from_string(string: str):

        attr_map = {member.value: member for member in AttributeModifier}

        result = attr_map.get(string)

        if result is None:
            result = AttributeModifier.NONE

        return result


class ClassAttribute:

    def __init__(self, is_method: bool, modifier: AttributeModifier, text: str):
        self.isMethod = is_method
        self.modifier = modifier
        self.text = text
