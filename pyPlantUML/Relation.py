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
