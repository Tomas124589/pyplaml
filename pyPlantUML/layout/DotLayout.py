from networkx.drawing.nx_agraph import graphviz_layout

from .DiagramLayout import DiagramLayout
from .. import Diagram

class DotLayout(DiagramLayout):

    def __init__(self, diagram: Diagram) -> None:
        self.diagram = diagram

    def apply(self) -> None:

        layout = graphviz_layout(self.getGraph(), prog='dot')

        for key, pos in layout.items():
            self.diagram.objects[key].x = pos[0]
            self.diagram.objects[key].y = pos[1]
