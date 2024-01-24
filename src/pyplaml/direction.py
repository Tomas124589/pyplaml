from enum import Enum

import manim


class Direction(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"

    def get_manim_vect_dir(self):
        if self == Direction.TOP:
            return manim.UP
        elif self == Direction.BOTTOM:
            return manim.DOWN
        elif self == Direction.LEFT:
            return manim.LEFT
        elif self == Direction.RIGHT:
            return manim.RIGHT
