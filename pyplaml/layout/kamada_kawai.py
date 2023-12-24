import networkx as nx

from .diagram_layout import DiagramLayout


class KamadaKawai(DiagramLayout):

    def apply(self) -> None:
        layout = nx.kamada_kawai_layout(self.get_graph())

        for key, pos in layout.items():
            self.diagram[key].x = pos[0]
            self.diagram[key].y = pos[1]
