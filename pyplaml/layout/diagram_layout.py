from __future__ import annotations

from abc import ABC, abstractmethod
import networkx as nx

from .. import Diagram
from ..diagram_object import PositionedDiagramObject


class DiagramLayout(ABC):

    def __init__(self, diagram: Diagram) -> None:
        self.diagram = diagram

    @abstractmethod
    def apply(self) -> DiagramLayout:
        pass

    def get_graph(self) -> nx.DiGraph:
        g = nx.DiGraph()
        for name, obj in self.diagram.objects.items():
            if isinstance(obj, PositionedDiagramObject) and obj.do_draw:
                g.add_node(name)
                if hasattr(obj, 'edges'):
                    for e in obj.edges:
                        g.add_edge(name, e.target.get_key())
        return g

    def scale(self, x: float, y: float) -> DiagramLayout:
        for name, obj in self.diagram.objects.items():
            if isinstance(obj, PositionedDiagramObject):
                self.diagram[name].x = self.diagram[name].x * x
                self.diagram[name].y = self.diagram[name].y * y
        return self
