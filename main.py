from manim import *
import pyplaml
import argparse


class MainScene(pyplaml.Scene):
    def anims(self):
        pass


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog="pyplaml")

    argparser.add_argument("file")
    argparser.add_argument("-a", "--animate", action="store_true")
    argparser.add_argument("-sx", "--scale-x", default=1, type=float)
    argparser.add_argument("-sy", "--scale-y", default=1, type=float)
    argparser.add_argument("-fps", "--frames-per-second", default=60, type=int)
    argparser.add_argument("-fcache", "--flush-cache", action="store_true")
    argparser.add_argument("-l", "--layout", choices=["dot", "spring"], default="dot")

    args = argparser.parse_args()

    src_file = Path(args.file)

    if not src_file.is_file():
        raise Exception("\"{}\" is not a file.".format(args.file))

    config.output_file = src_file.stem
    config.cairo_path = "media/images/"
    config.ffmpeg_path = "media/videos/"
    config.frame_rate = args.frames_per_second
    config.flush_cache = args.flush_cache

    scene = MainScene()

    scene.file = args.file
    scene.animate = args.animate
    scene.scale_x = args.scale_x
    scene.scale_y = args.scale_y
    scene.layout = args.layout

    scene.render()
