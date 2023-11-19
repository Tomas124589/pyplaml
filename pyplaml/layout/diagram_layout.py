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

            for e in obj.edges:
                g.add_edge(name, e.target.name)

        return g

    def scale(self, x: float, y: float) -> None:
        for name, obj in self.diagram.objects.items():
            self.diagram.objects[name].x = self.diagram.objects[name].x * x
            self.diagram.objects[name].y = self.diagram.objects[name].y * y
