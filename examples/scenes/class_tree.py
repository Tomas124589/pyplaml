from pyplaml import *


class MyScene(ZoomedScene):
    def construct(self):
        self.camera.background_color = WHITE
        Text.set_default(font_size=16)

        diag = PUMLParser().parse_file("examples/plantuml/02_class_tree.puml")
        diag.layout = DotLayout()
        diag.apply_layout(1.5, 1.2)

        self.add(diag)
        self.camera.auto_zoom(self.mobjects, margin=1, animate=False)

        self.play(diag["C5"].animate.shift(LEFT*2))
        self.play(diag["C7"].animate.shift(UP*2))

        self.wait(2)
