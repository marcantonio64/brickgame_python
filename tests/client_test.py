"""
Testing some `client.py` elements.

See `screens_test.py` for ``BaseClient.load_image()``.
"""

import sys
import tkinter as tk
from ..constants import *
from ..client import *


class Client1(BaseClient):
    """ A (theoretically) functioning client: plain. """

    pass


class Client2(BaseClient):
    """ A (theoretically) functioning client: title. """

    def __init__(self):
        super().__init__()
        self.window.title("Title test")
        self.canvas.config(background=SHADE_COLOR)


class Client3(BaseClient):
    """ A (theoretically) functioning client: simple mechanics. """

    def __init__(self):
        self.j = 1
        super().__init__()
        self.draw_square(0, 0)

    def draw_square(self, i, j):
        """ Draw an empty square. """
        self.canvas.create_rectangle(
            i*DIST_BLOCKS,
            j*DIST_BLOCKS,
            i*DIST_BLOCKS+BLOCK_SIDE,
            j*DIST_BLOCKS+BLOCK_SIDE,
            fill=BACK_COLOR,
            width=PIXEL_SIDE,
            outline=LINE_COLOR,
            )

    def loop(self):
        """ List of scheduled events. """

        if self.ticks % FPS == 0:  # Every second, do...
            self.j += 1
            # Create another square below the previous ones.
            self.draw_square(0, self.j)


class Client4:
    pass


class Client5:
    window = None
    canvas = None


class Client6:
    window = "window"
    canvas = 0


class Client7:
    window = tk.Tk
    canvas = tk.Canvas


class Client8:
    window = tk.Tk()
    canvas = tk.Canvas


class Client9:
    window = tk.Tk()
    canvas = tk.Canvas(tk.Tk())


class Client10:
    window = None
    canvas = None
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window)


class Client11:
    window = None
    canvas = None
    def __init__(self):
        Client11.window = tk.Tk()
        Client11.canvas = tk.Canvas(Client11.window)


def main(args):
    """ Output-generating commands. """

    if len(args) != 2:
        print("Please provide one argument to specify the class, for example:")
        print("python -m brickgame_python.tests.client_test 1")
    else:
        try:
            m = int(args[1])
        except ValueError:
            print("The argument should be a positive integer.")
            exit()
        if m:
            if int(m) < 4:
                # Testing `BaseClient`'s implementations
                exec(f"client = Client{m}(); client.start()")
            elif int(m) < 12:
                # Testing `has_window_and_canvas()`
                exec(f"client = Client{m}(); print(has_window_and_canvas(Client{m}))")
            else:
                print(f"Client{m} was not implemented yet.")
        else:
            print(AbsentWindowOrCanvasError("arg"))
            raise AbsentWindowOrCanvasError("arg")


if __name__ == '__main__':
    main(sys.argv)
