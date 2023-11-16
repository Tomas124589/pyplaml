import networkx as nx

from .DiagramLayout import DiagramLayout
from .. import Diagram

class KamadaKawai(DiagramLayout):

    def __init__(self, diagram: Diagram) -> None:
        self.diagram = diagram

    def apply(self) -> None:

        layout = nx.kamada_kawai_layout(self.getGraph())

        for key, pos in layout.items():
            self.diagram.objects[key].x = pos[0]
            self.diagram.objects[key].y = pos[1]
