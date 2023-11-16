import networkx as nx

from .DiagramLayout import DiagramLayout


class SpringLayout(DiagramLayout):

    def apply(self) -> None:
        layout = nx.spring_layout(self.get_graph())

        for key, pos in layout.items():
            self.diagram.objects[key].x = pos[0]
            self.diagram.objects[key].y = pos[1]
