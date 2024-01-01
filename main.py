from manim import *

from pyplaml import *

import argparse

from pyplaml.layout.spring_layout import SpringLayout
from pyplaml.layout.dot_layout import DotLayout


class MainScene(MovingCameraScene):
    file: str
    animate: bool
    scale_x: float
    scale_y: float

    def construct(self):
        parser = PUMLParser()
        d: Diagram = parser.parse_file(self.file)

        layout = DotLayout(d)
        layout.apply()
        layout.scale(self.scale_x, self.scale_y)

        self.camera.background_color = WHITE
        Text.set_default(font_size=16)

        d.set_scene(self)

        d.animate = self.animate

        d.draw()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog="pyplaml")

    argparser.add_argument("file")
    argparser.add_argument("-a", "--animate", action="store_true")
    argparser.add_argument("-sx", "--scale-x", default=1, type=float)
    argparser.add_argument("-sy", "--scale-y", default=1, type=float)

    args = argparser.parse_args()

    src_file = Path(args.file)

    if not src_file.is_file():
        raise Exception("\"{}\" is not a file.".format(args.file))

    config.output_file = src_file.stem
    config.cairo_path = "media/images/"
    config.ffmpeg_path = "media/videos/"

    scene = MainScene()

    scene.file = args.file
    scene.animate = args.animate
    scene.scale_x = args.scale_x
    scene.scale_y = args.scale_y

    scene.render()
