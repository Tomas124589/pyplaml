import pyplaml
from pyplaml.diagram_class import *


class MyScene(pyplaml.Scene):
    def prepare_diagram(self) -> Diagram:
        self.set_layout('dot')

        d = Diagram()

        c1 = DiagramClass('Class1').append_to_diagram(d)
        c2 = DiagramClass('Class2').append_to_diagram(d)
        c1.edges.append(DiagramEdge(False).between(c1, c2).append_to_diagram(d))

        return d

    def anims(self):
        self.play(self.moa('Class1').shift(2 * LEFT).rotate(45 * DEGREES), run_time=2)
        self.play(self.camera.auto_zoom(self.mobjects))
        self.play(self.moa('Class1').shift(UP).rotate(90 * DEGREES), run_time=2)
        self.play(self.moa('Class1').rotate(45 * DEGREES), run_time=1)
        self.play(self.moa('Class1').rotate(90 * DEGREES), run_time=1)
        self.play(self.moa('Class1').rotate(90 * DEGREES), run_time=2)

        self.play(self.moa('Class2').shift(DOWN * 2).rotate(45 * DEGREES), run_time=2)
        self.play(self.moa('Class2').rotate(45 * DEGREES), run_time=1)
        self.play(self.moa('Class2').rotate(45 * DEGREES), run_time=1)
        self.play(self.moa('Class2').rotate(45 * DEGREES), run_time=1)
        self.play(self.moa('Class2').rotate(90 * DEGREES), run_time=2)
        self.play(self.moa('Class2').rotate(90 * DEGREES), run_time=2)

        self.wait(3)
