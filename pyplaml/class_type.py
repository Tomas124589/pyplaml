from enum import Enum


class ClassType(Enum):
    CLASS = "class"
    ENTITY = "entity"
    ENUM = "enum"
    EXCEPTION = "exception"
    INTERFACE = "interface"
    META_CLASS = "metaclass"
    PROTOCOL = "protocol"
    STEREOTYPE = "stereotype"
    STRUCT = "struct"

    @staticmethod
    def from_string(string: str):
        attr_map = {member.value: member for member in ClassType}
        return attr_map.get(string)
