from __future__ import annotations

from abc import ABC, abstractmethod

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

from pyplaml import Diagram
from pyplaml.diagram_object import PositionedDiagramObject


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


class DotLayout(DiagramLayout):
    def apply(self):
        layout = graphviz_layout(self.get_graph(), prog='dot')

        scale_x, scale_y = self.calculate_scaling_factors(layout)

        for key, pos in layout.items():
            self.diagram[key].x = pos[0] * scale_x * 2
            self.diagram[key].y = pos[1] * scale_y * 2

        return self

    @staticmethod
    def calculate_scaling_factors(layout):
        x_distances = []
        y_distances = []
        for key1, pos1 in layout.items():
            for key2, pos2 in layout.items():
                if key1 != key2:
                    x_distance = abs(pos1[0] - pos2[0])
                    y_distance = abs(pos1[1] - pos2[1])
                    x_distances.append(x_distance)
                    y_distances.append(y_distance)

        if x_distances and y_distances:
            average_x_distance = sum(x_distances) / len(x_distances)
            average_y_distance = sum(y_distances) / len(y_distances)

            x_scaling_factor = 1.0 / average_x_distance if average_x_distance != 0 else 1.0
            y_scaling_factor = 1.0 / average_y_distance if average_y_distance != 0 else 1.0

            return x_scaling_factor, y_scaling_factor
        else:
            return 1.0, 1.0


class SpringLayout(DiagramLayout):
    def apply(self):
        layout = nx.spring_layout(self.get_graph())

        for key, pos in layout.items():
            self.diagram[key].x = pos[0]
            self.diagram[key].y = pos[1]

        return self


class DiagramLayoutFactory:
    @staticmethod
    def make(name: str, diagram: Diagram):
        if name == 'dot':
            return DotLayout(diagram)
        elif name == 'spring':
            return SpringLayout(diagram)

        raise Exception('Undefined layout "{}"'.format(name))
