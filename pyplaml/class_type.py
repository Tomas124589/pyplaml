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
    META_CLASS = "metaclass"
    PROTOCOL = "protocol"
    STEREOTYPE = "stereotype"
    STRUCT = "struct"

    @staticmethod
    def from_string(string: str) -> ClassType:
        _type = {member.value: member for member in ClassType}.get(string)
        return ClassType.UNKNOWN if _type is None else _type
