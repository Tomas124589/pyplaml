from pyplaml import *
from pyplaml.diagram_layout import *


class MyScene(Scene):
    def anims(self):
        c1 = DiagramClass('C1')
        c2 = DiagramClass('C2')
        c3 = DiagramClass('C3')

        c2.add_edge(DiagramEdge(False, c2, c1, target_rel=Relation.EXTENSION))
        c3.add_edge(DiagramEdge(True, c3, c1, target_rel=Relation.ASSOCIATION))

        diagram = Diagram(DotLayout())
        diagram.add(c1, c2, c3, c2.get_edge_to(c1), c3.get_edge_to(c1))
        diagram.apply_layout(3, 2)

        self.add(diagram)

        self.camera.auto_zoom(self.mobjects, animate=False)
