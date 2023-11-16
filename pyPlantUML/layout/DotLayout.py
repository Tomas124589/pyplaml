from networkx.drawing.nx_agraph import graphviz_layout

from .DiagramLayout import DiagramLayout


class DotLayout(DiagramLayout):

    def apply(self) -> None:
        layout = graphviz_layout(self.get_graph(), prog='dot')

        for key, pos in layout.items():
            self.diagram.objects[key].x = pos[0]
            self.diagram.objects[key].y = pos[1]
