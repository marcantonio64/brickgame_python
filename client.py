""" Establishing the basic structure of the client. """

import os
import tkinter as tk
from _tkinter import TclError
from PIL import Image, ImageTk
from abc import ABC
from .constants import *

__all__ = ["BaseClient",
           "Screen",
           "AbsentWindowOrCanvasError",
           "has_window_and_canvas",
           "package_dir",
           "screens_dir",
           ]

package_dir = os.path.abspath(
    os.path.dirname(__file__)
)
""" Directory of the main package. """
screens_dir = os.path.join(package_dir, "screens")
""" Directory of the screens/ folder. """


class BaseClient(ABC):
    """
    General GUI and loop configs.

    Attributes
    ----------
    window : tk.Tk
        A `tkinter.Tks <https://tkdocs.com/pyref/tk.html>`_ object.
    canvas : tk.Canvas
        A `tkinter.Canvas <https://tkdocs.com/pyref/canvas.html>`_ object.
    """

    window = None
    canvas = None

    def __init__(self):
        """ Initialize a GUI, place a `canvas`, and read user input. """

        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.config(cursor="")  # Hiding the cursor.
        self.canvas = tk.Canvas(self.window,
                                width=WINDOW_WIDTH,
                                height=WINDOW_HEIGHT,
                                background=BACK_COLOR)
        self.canvas.grid()

        # Since all drawings are made to one screen, we use the shared
        # class variables.
        BaseClient.window = self.window
        BaseClient.canvas = self.canvas

        # Read user input.
        self.window.bind(
            "<KeyPress>",
            lambda event: self._handle_events(event, True)
        )
        self.window.bind(
            "<KeyRelease>",
            lambda event: self._handle_events(event, False)
        )

        self.ticks = 0

    def _loop(self):
        """ A hidden method avoids looping the parent class instead. """

        self.ticks += 1
        self.loop()
        # A canvas.after() call to the same function creates a loop.
        after_id = self.canvas.after(TICK_RATE, self._loop)
        # Making sure the program ends when the window is closed.
        def close():
            self.canvas.after_cancel(after_id)
            self.window.quit()
        self.window.protocol("WM_DELETE_WINDOW", close)

    def _handle_events(self, event, press):
        """
        Set up the structure for input events.

        Parameters
        ----------
        event : tk.Event
            A key id.
        press : bool
            Whether the key was pressed or released.
        """

        # Convert the event to str.
        key = event.keysym.lower()

        # Window exit condition.
        if press and key == "escape":
            self.window.quit()
        else:
            self.handle_events(key, press)

    def start(self):
        self._loop()
        self.window.mainloop()

    def loop(self):
        """ Scheduling looping events. """

        pass

    def handle_events(self, key, press):
        """
        Deal with user input.

        Parameters
        ----------
        key : str
            Current key.
        press : bool
            Whether the key was pressed or released.
        """

        pass


class Screen:
    """ Manages image importing. """

    def __init__(self, source):
        """
        Constructor for :class:`Screen` instances.

        Parameters
        ----------
        source : Type[Client]
            A class with ``window`` and ``canvas`` attributes.
        """

        self.__lazy_img = None
        self.__image = None
        self.__images = []
        self.__i = 0
        self.window = source.window
        self.canvas = source.canvas

    def load_image(self, image_prefix, tags=""):
        """
        Accessing images from `screens/`.

        Parameters
        ----------
        image_prefix : str
            Name prefix (without the `-wxh.png`) identifying the image.
        tags : str, optional
            Grouping id for tkinter objects. Defaults to ``""``.
        """

        file = os.path.join(
            screens_dir,
            "{0}-{1}x{2}.png".format(image_prefix, WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        if not os.path.exists(file):
            print("File", file, "doesn't exist")
            pass
        try:
            self.__lazy_img = Image.open(file)
            self.__image = ImageTk.PhotoImage(self.__lazy_img)
            self.__images.extend((self.__lazy_img, self.__image))
            self.canvas.create_image(WHITE_BORDER,
                                     WHITE_BORDER,
                                     anchor=tk.NW,
                                     image=self.__image,
                                     tags=tags,
                                     )
        except TclError:
            pass


class AbsentWindowOrCanvasError(Exception):
    """ Missing or undefined `.window` or `.canvas`. """
    def __init__(self, arg):
        """ Missing or undefined `.window` or `.canvas`. """
        super().__init__(
            f"`{arg}` should have a `tkinter.Tk` and a `tkinter.Canvas` class variables."
        )


def has_window_and_canvas(arg):
    """ Check for ``arg.window`` and ``arg.canvas``. """
    if hasattr(arg, "window") and hasattr(arg, "canvas"):
        if isinstance(arg.window, tk.Tk) and isinstance(arg.canvas, tk.Canvas):
            return True
    return False
