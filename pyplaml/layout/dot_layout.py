from networkx.drawing.nx_agraph import graphviz_layout

from .diagram_layout import DiagramLayout


class DotLayout(DiagramLayout):

    def apply(self) -> None:
        layout = graphviz_layout(self.get_graph(), prog='dot')

        for key, pos in layout.items():
            self.diagram[key].x = pos[0]
            self.diagram[key].y = pos[1]
