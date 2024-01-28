from __future__ import annotations

from abc import ABC, abstractmethod

import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

from pyplaml import *


class DiagramLayout(ABC):
    objects: typing.Dict[str, DiagramObject]

    @abstractmethod
    def apply(self, objects: typing.Dict[str, DiagramObject], scale_x: float = 1, scale_y: float = 1):
        self.objects = objects

    def get_graph(self) -> nx.DiGraph:
        g = nx.DiGraph()
        for name, o in self.objects.items():
            g.add_node(o.get_key())
            for e in o.edges:
                g.add_edge(e.target.get_key(), o.get_key())
        return g


class DotLayout(DiagramLayout):
    def apply(self, objects: typing.Dict[str, DiagramObject], scale_x: float = 1, scale_y: float = 1):
        super().apply(objects)
        layout = graphviz_layout(self.get_graph(), prog="dot")
        x, y = self.calculate_scaling_factors(layout)

        for key, pos in layout.items():
            layout[key] = (pos[0] * scale_x * x * 2, pos[1] * scale_y * y * 2)

        return layout

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
    def apply(self, objects: typing.Dict[str, DiagramObject], scale_x: float = 1, scale_y: float = 1):
        super().apply(objects)
        return nx.spring_layout(self.get_graph())
