from enum import Enum


class AttributeModifier(Enum):
    NONE = ""
    PRIVATE = "-"
    PACKAGE_PRIVATE = "~"
    PROTECTED = "#"
    PUBLIC = "+"

    def fromString(string: str):

        attrMap = {member.value: member for member in AttributeModifier}

        result = attrMap.get(string)

        if result is None:
            result = AttributeModifier.NONE

        return result


class ClassAttribute:

    def __init__(self, isMethod: bool, modifier: AttributeModifier, text: str):
        self.isMethod = isMethod
        self.modifier = modifier
        self.text = text
