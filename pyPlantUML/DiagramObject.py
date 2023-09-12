from __future__ import annotations

from abc import ABC, abstractmethod

from typing import List

from manim import *


class DiagramObject(ABC):

    def __init__(self, name: str):
        self.objects: List[DiagramObject] = []
        self.lines: typing.Dict[DiagramObject, List[DiagramLine]] = {}
        self.name = name
        self.mobject: Mobject = None
        self.doCustomPosition = False

    @abstractmethod
    def draw(self) -> Mobject:
        pass

    def addObject(self, obj: DiagramObject):
        if not isinstance(obj, DiagramObject):
            raise Exception("Invalid type")
        self.objects.append(obj)

    def addLine(self, line: DiagramLine):

        if line.target not in self.lines:
            self.lines[line.target] = []
            
        self.lines[line.target].append(line)

    def __str__(self):

        objCount = len(self.objects)
        linesCount = len(self.lines)

        result = self.__class__.__name__ + "\n"
        result += "Name: '" + self.name + "'\n"
        result += "Objects: " + str(objCount) + "\n"
        result += "Lines: " + str(linesCount)

        if objCount > 0:

            for child in self.objects:
                result += '\n\t'.join(("\n" + str(child)).splitlines())
                result += "\n"

        return result

    def __hash__(self):
        return hash(str(self))