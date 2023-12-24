from abc import ABC, abstractmethod

import networkx as nx

from .. import Diagram


class DiagramLayout(ABC):

    def __init__(self, diagram: Diagram) -> None:
        self.diagram = diagram

    @abstractmethod
    def apply(self) -> None:
        pass

    def get_graph(self) -> nx.DiGraph:
        g = nx.DiGraph()
        for name, obj in self.diagram.objects.items():
            g.add_node(name)
            if hasattr(obj, 'edges'):
                for e in obj.edges:
                    g.add_edge(name, e.target.get_key())
        return g

    def scale(self, x: float, y: float) -> None:
        for name, obj in self.diagram.objects.items():
            self.diagram[name].x = self.diagram[name].x * x
            self.diagram[name].y = self.diagram[name].y * y
