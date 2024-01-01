from enum import Enum


class Relation(Enum):
    NONE = 0
    EXTENSION = 1
    ASSOCIATION = 2
    AGGREGATION = 3
    COMPOSITION = 4
    HASH = 5
    CROSS = 6
    CROW_FOOT = 7
    NEST_CLASSIFIER = 8

    @staticmethod
    def from_string(string: str | None):
        if string is None:
            return Relation.NONE

        if string in ['<|', '|>', '^']:
            return Relation.EXTENSION
        elif string in ['<', '>']:
            return Relation.ASSOCIATION
        elif string in ['o']:
            return Relation.AGGREGATION
        elif string in ['*']:
            return Relation.COMPOSITION
        elif string in ['#']:
            return Relation.HASH
        elif string in ['x']:
            return Relation.CROSS
        elif string in ['{', '}']:
            return Relation.CROW_FOOT
        elif string in ['+']:
            return Relation.NEST_CLASSIFIER
        else:
            raise Exception('Undefined relation "{}"'.format(string))
