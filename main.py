import argparse

from manim import *

from pyplaml import PUMLParser
from pyplaml.diagram_layout import DotLayout


class MainScene(ZoomedScene):
    file: str
    scale_x: float
    scale_y: float

    def construct(self):
        self.camera.background_color = WHITE
        Text.set_default(font_size=16)

        diagram = PUMLParser().parse_file(self.file)
        diagram.layout = DotLayout()
        diagram.apply_layout(self.scale_x, self.scale_y)

        self.add(diagram)

        self.camera.auto_zoom(self.mobjects, margin=0.5, animate=False)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog="pyplaml")

    argparser.add_argument("file", help="Path to .puml file")
    argparser.add_argument("-sx", "--scale-x", default=1, type=float, help="Scale for x-axis")
    argparser.add_argument("-sy", "--scale-y", default=1, type=float, help="Scale for y-axis")

    args = argparser.parse_args()

    src_file = Path(args.file)

    if not src_file.is_file():
        raise FileNotFoundError(f"File not found: {args.file}")

    config.output_file = src_file.stem

    scene = MainScene()

    scene.file = args.file
    scene.scale_x = args.scale_x
    scene.scale_y = args.scale_y

    scene.render()
