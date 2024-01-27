from __future__ import annotations

from enum import Enum


class ClassType(Enum):
    UNKNOWN = "unknown"
    CLASS = "class"
    ANNOTATION = "annotation"
    ENTITY = "entity"
    ENUM = "enum"
    EXCEPTION = "exception"
    INTERFACE = "interface"
    METACLASS = "metaclass"
    PROTOCOL = "protocol"
    STEREOTYPE = "stereotype"
    STRUCT = "struct"
    OBJECT = "object"

    @staticmethod
    def from_string(string: str) -> ClassType:
        return ClassType.__members__.get(string.upper(), ClassType.UNKNOWN)
