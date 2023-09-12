from __future__ import annotations

from abc import ABC, abstractmethod

from typing import List

from manim import *


class DiagramNode(ABC):

    def __init__(self, name: str):
        self.nodes: List[DiagramNode] = []
        self.lines: typing.Dict[DiagramNode, List[DiagramLine]] = {}
        self.name = name
        self.mobject: Mobject = None
        self.doCustomPosition = False

    @abstractmethod
    def draw(self) -> Mobject:
        pass

    def addNode(self, node: DiagramNode):
        if not isinstance(node, DiagramNode):
            raise Exception("Invalid type")
        self.nodes.append(node)

    def addLine(self, line: DiagramLine):

        if line.target not in self.lines:
            self.lines[line.target] = []
            
        self.lines[line.target].append(line)

    def __str__(self):

        childCount = len(self.nodes)
        linesCount = len(self.lines)

        result = self.__class__.__name__ + "\n"
        result += "Name: '" + self.name + "'\n"
        result += "Nodes: " + str(childCount) + "\n"
        result += "Lines: " + str(linesCount)

        if childCount > 0:

            for child in self.nodes:
                result += '\n\t'.join(("\n" + str(child)).splitlines())
                result += "\n"

        return result

    def __hash__(self):
        return hash(str(self))