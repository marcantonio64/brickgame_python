""" This module contains an implementation of a Tetris game. """

import random
from ..constants import *
from ..client import BaseClient, Screen
from ..block import Block
from . import game_manuals
from .game_engine import Game

__doc__ = "".join([__doc__, "\n\nCheck `", game_manuals, "` for instructions."])
__all__ = ["Tetris"]


class Tetris(Game):
    """
    Implements `Game` with a Tetris game.

    Attributes
    ----------
    canvas : tkinter.Canvas
        The current `Canvas`.
    start_speed : int
        Storing the starting value for ``self.speed``.
    entities : dict
        Containers for the objects to be drawn (tag:list).
    """

    start_speed = 1
    entities = {"piece": [], "fallen": []}

    def __init__(self, source):
        """
        Initialize instance attributes and instantiate game objects.

        Parameters
        ----------
        source : type[Client]
            A class with ``window`` and ``canvas`` attributes.

        Raises
        ------
        AbsentWindowOrCanvasError
            If the ``source`` parameter has incorrect ``window`` or ``canvas`` attributes.
        """

        super().__init__(source)
        self.__start = 1
        self.speed = Tetris.start_speed  # Fall speed (in `Block`s per second).

        # Spawn the entities.
        self.piece = self.Piece()  # Tetrominoes
        self.fallen = self.FallenBlocks()  # Fallen remains

        # Identify this game's objects with a tag.
        self.add_tags()

    def _detect_game_on(self):
        """ Prints a first preview only when the game is played. """

        if not self.__start:
            self.piece.print_preview()
        self.__start -= 1
    
    def handle_events(self, key, press):
        """
        Set the keybindings.

        Parameters
        ----------
        key : str
            Current key.
        press : bool
            Whether the key was pressed or released.
        """

        super().handle_events(key, press)

        if self.running:
            if press:  # Key pressed.
                # Set `Piece`'s movement.
                if key == "up":
                    self.piece.rotate()
                elif key == "down":
                    self.Piece.direction = "down"
                elif key == "left":
                    self.Piece.direction = "left"
                elif key == "right":
                    self.Piece.direction = "right"
                elif key == "space":
                    self.piece.fall_inst()
                    self.spawn_next()
                elif key == "shift_r":
                    if not self.piece.lock_switch:
                        # Only once for every new piece.
                        self.piece.switch()

            else:  # Key released.
                if key == "down":
                    self.Piece.direction = ""
                elif key == "left":
                    self.Piece.direction = ""
                elif key == "right":
                    self.Piece.direction = ""
    
    def manage(self, t):
        """
        Game logic implementation.

        Parameters
        ----------
        t : int
            A timer.
        """

        if self.running and not self.paused:
            self._detect_game_on()
            # Set the action rate at `speed` `Block`s per second.
            if t % int(FPS/self.speed) == 0:
                self.piece.move("down")  # Slow fall
                self.try_spawn_next()

            # `speed` scales over time, every 30 seconds.
            if self.speed <= 10:
                if t % (30*FPS) == 0:
                    self.speed *= 10**0.05
            
            # Adjust for movement proportional to the scaling speed
            if t % int(FPS/(7 + 3*self.speed)) == 0:
                # Horizontal movement and downwards acceleration.
                self.piece.move(self.piece.direction)
        
        super().manage()  # Manage endgame.
    
    def update_score(self, full_lines_number):
        """ Scoring mechanics. """
        
        # More points for more lines at once.
        if full_lines_number == 1:
            self.score += int(2 + self.speed*self.fallen.height)*15
        elif full_lines_number == 2:
            self.score += int(6 + self.speed*self.fallen.height)*15
        elif full_lines_number == 3:
            self.score += int(12 + self.speed*self.fallen.height)*15
        elif full_lines_number == 4:
            self.score += int(20 + self.speed*self.fallen.height)*15
        super().update_score()
    
    def try_spawn_next(self):
        """ `piece`s spawn when they stop falling. """
        
        if self.piece.height == 0:
            self.spawn_next()
    
    def spawn_next(self):

        # Transfer the `piece`'s `Block`s to the `fallen` structure.
        self.fallen.grow()
        # Account for a proper score according to the lines cleared.
        full_lines_number = self.fallen.remove_full_lines()
        self.update_score(full_lines_number)
        
        # Reset `height` and spawn a new `Piece` object.
        self.piece.height = 18
        self.piece = self.Piece()
        self.piece.print_preview()
    
    def check_victory(self):
        """
        The game is endless, except for defeat.

        Returns
        -------
        bool
            Whether the game has been beaten.
        """

        return False
    
    def check_defeat(self):
        """
        Defeat happens if the `fallen` structure reaches the top of the grid.

        Returns
        -------
        bool
            Whether the game was lost.
        """

        return self.fallen.height > 20
    
    class Piece:
        """
        Organizes the four-tiled-piece's mechanics.

        Attributes
        ----------
        direction : str
            Where to move the piece (``"left"``,``"right"``,  or
            ``"down"`` to accelerate the fall).
        stored_shape : str
            A character representing the next `Tetris.Piece`'s shape.
        """

        direction = ""
        stored_shape = ""
        blocks = {}
        coords = None
        piece = None
        
        def __init__(self):
            self.height = 19
            self.lock_switch = False

            # If there is any `stored_shape`, store its value into
            # `active_shape`.
            if Tetris.Piece.stored_shape:
                self.active_shape = Tetris.Piece.stored_shape
            else:
                # Otherwise, choose the value of `active_shape`
                # randomly.
                self.active_shape = random.choice(
                    ("T", "J", "L", "S", "Z", "I", "O")
                )
            # Store a new shape.
            Tetris.Piece.stored_shape = random.choice(
                ("T", "J", "L", "S", "Z", "I", "O")
            )
            # Spawn a `Piece` object with the `active_shape`.
            self.spawn()
            # Permit one switch between `active_shape` and
            # `stored_shape`.
            self.lock_switch = False
        
        def spawn(self):
            """ Draw the desired piece on the screen, at top center. """

            self.place(self.active_shape, 4, 0)
            # Identify the next rotated position.
            self.next_id, self.piece_coords = self.blocks[1]
            Tetris.entities["piece"] = [
                Block(i, j, Tetris.source, tags="piece")
                for (i, j) in self.piece_coords
            ]
        
        def print_preview(self):
            """ Showcase `stored_shape`. """

            if Tetris.Piece.stored_shape == "T":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    "    _\n",
                    " _ |_| _\n",
                    "|_||_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "J":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    " _\n",
                    "|_| _  _\n",
                    "|_||_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "L":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    "       _\n",
                    " _  _ |_|\n",
                    "|_||_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "S":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    "    _  _\n",
                    " _ |_||_|\n",
                    "|_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "Z":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    " _  _\n",
                    "|_||_| _\n",
                    "   |_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "I":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    " _  _  _  _\n",
                    "|_||_||_||_|"
                ])
                print(drawing)
            elif Tetris.Piece.stored_shape == "O":
                drawing = "".join([
                    "=============\n"
                    "Next:\n",
                    " _  _\n",
                    "|_||_|\n",
                    "|_||_|"
                ])
                print(drawing)
        
        def switch(self):
            """
            Mechanics for switching pieces.

            Change a `piece` with `active_shape` to one with
            `stored_shape` (only once for each new spawn).
            """

            # Clear the current `piece`'s drawing and references.
            Tetris.canvas.delete("piece")
            Tetris.entities["piece"] = []
            # Switch shapes.
            a = self.active_shape
            s = Tetris.Piece.stored_shape
            self.active_shape = s
            Tetris.Piece.stored_shape = a
            # Reset `height`.
            self.height = 19

            self.spawn()
            self.print_preview()
            
            self.lock_switch = True  # Only once for every new `piece`.
        
        def place(self, shape, i, j):
            """
            Positioning of `Block`s to form each shape and track rotation.

            Parameters
            ----------
            shape : str
                A character representing the desired shape.
            i : int
                Horizontal coordinate reference.
            j : int
                Vertical coordinate reference.
            """
            
            self.coords = (i, j)
            if shape == "T":
                self.blocks = {
                    1: (2, ((i-1, j), (i, j), (i+1, j), (i, j-1))),
                    2: (3, ((i-1, j), (i, j), (i, j-1), (i, j+1))),
                    3: (4, ((i-1, j), (i, j), (i+1, j), (i, j+1))),
                    4: (1, ((i, j-1), (i, j), (i+1, j), (i, j+1)))
                }
            elif shape == "J":
                self.blocks = {
                    1: (2, ((i-1, j-1), (i-1, j), (i, j), (i+1, j))),
                    2: (3, ((i, j-1), (i, j), (i, j+1), (i-1, j+1))),
                    3: (4, ((i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j))),
                    4: (1, ((i-1, j-1), (i, j-1), (i-1, j), (i-1, j+1)))
                }
            elif shape == "L":
                self.blocks = {
                    1: (2, ((i-1, j), (i, j), (i+1, j), (i+1, j-1))),
                    2: (3, ((i-1, j-1), (i, j-1), (i, j), (i, j+1))),
                    3: (4, ((i-1, j), (i-1, j-1), (i, j-1), (i+1, j-1))),
                    4: (1, ((i-1, j-1), (i-1, j), (i-1, j+1), (i, j+1)))
                }
            elif shape == "S":
                self.blocks = {
                    1: (2, ((i-1, j), (i, j), (i, j-1), (i+1, j-1))),
                    2: (1, ((i, j+1), (i, j), (i-1, j), (i-1, j-1)))
                }
            elif shape == "Z":
                self.blocks = {
                    1: (2, ((i-1, j-1), (i, j-1), (i, j), (i+1, j))),
                    2: (1, ((i, j - 1), (i, j), (i-1, j), (i-1, j+1)))
                }
            elif shape == "I":
                self.blocks = {
                    1: (2, ((i-1, j), (i, j), (i+1, j), (i+2, j))),
                    2: (1, ((i, j-1), (i, j), (i, j+1), (i, j+2)))
                }
            elif shape == "O":
                self.blocks = {
                    1: (1, ((i, j), (i, j+1), (i+1, j), (i+1, j+1)))
                }

        def calculate_dimensions(self):
            """
            Track the boundary dimensions of each `Piece` and update `height`.

            Returns
            -------
            tuple[int, int, int]
                Horizontal and vertical limits.
            """

            try:
                i_min = min(
                    [block.coords[0] for block in Tetris.entities["piece"]]
                )
                i_max = max(
                    [block.coords[0] for block in Tetris.entities["piece"]]
                )
                j_max = max(
                    [block.coords[1] for block in Tetris.entities["piece"]]
                )
                
                # Calculation of `height`:
                heights = []
                for i in range(i_min, i_max+1):
                    # For each horizontal coordinate,...
                    piece_col = [block.coords[1]
                                 for block in Tetris.entities["piece"]
                                 if block.coords[0] == i]
                    # choose the piece's lowest vertical coordinate...
                    j = max([0] + piece_col)
                    # and the fallen structure's highest vertical coordinate.
                    fall_col = [block.coords[1]
                                for block in Tetris.entities["fallen"]
                                if block.coords[0] == i
                                and block.coords[1] > j]
                    # If there's anything below the piece in this column, ...
                    if fall_col:
                        # add the distance to the list of heights.
                        heights.append(min(fall_col)-j-1)
                    else:
                        # Otherwise, add the distance to the bottom of
                        # the grid to the list.
                        heights.append(19-j)
                # The `height` attribute is the shortest distance from
                # a piece to the fallen structure.
                self.height = min(heights)
                return i_min, i_max, j_max
            # In case any calculation fails, return dummy values.
            except ValueError:
                return 10, 10, 20
        
        def move(self, direction):
            """
            Check if there are obstacles for movement, move if not.

            Parameters
            ----------
            direction : str
                Where to move (``"left"``,``"right"``,  or
                ``"down"`` to accelerate the fall).
            """

            # Gatter all the necessary dimensions to detect whether
            # movement is possible.
            a, b = CONVERT[direction]
            i, j = self.coords
            i_min, i_max, j_max = self.calculate_dimensions()

            # First, build a set with the desired new positions for
            # each `Block` in the piece.
            X = set(
                [(block.coords[0]+a, block.coords[1]+b)
                 for block in Tetris.entities["piece"]]
            )
            # Second, build a set with the current positions of the
            # already formed structure.
            Y = set(
                [block.coords
                 for block in Tetris.entities["fallen"]]
            )
            # If those sets don't intersect, then movement can happen.
            if X & Y == set():
                # Check also if the movement won't get any `Block`
                # outside screen boundaries.
                if 0 <= i_min+a and i_max+a < 10 and j_max+b < 20:
                    # Update the `self.blocks` dict.
                    self.place(self.active_shape, i+a, j+b)
                    # Make the movement.
                    for block in Tetris.entities["piece"]:
                        i, j = block.coords
                        block.set_position(i+a, j+b)
        
        def rotate(self):
            """ Check if there are obstacles for rotation, rotate if not. """

            # First set: desired new positions of the piece's
            # `Block`s if rotation were to happen.
            X = set(self.blocks[self.next_id][1])
            # Second set: current positions of blocks in the
            # structure.
            Y = set(
                [block.coords for block in Tetris.entities["fallen"]]
            )
            # Third set: positions outside the borders in the
            # rotation.
            Z = set(
                [(i, j)
                 for (i, j) in X
                 if not (0 <= i < 10 and j < 20)]
            )
            # If the rotated piece doesn't collide with the
            # structure and remains inside the grid, then movement
            # occurs.
            if X & Y == set() and Z == set():
                # Erase the current piece from the screen.
                Tetris.canvas.delete("piece")
                # Replace it with another with the next rotated state.
                self.place(self.active_shape, *self.coords)
                # Update the rotating id and draw the piece's
                # `Block`s.
                self.next_id, self.piece_coords = self.blocks[self.next_id]
                Tetris.entities["piece"] = [
                    Block(i, j, Tetris.source, tags="piece")
                    for (i, j) in self.piece_coords
                ]
        
        def fall_inst(self):
            """ Instant fall, moving down a piece by its ``height``. """

            i, j = self.coords
            # Get current `height`.
            self.calculate_dimensions()
            # Update `blocks`.
            self.place(self.active_shape, i, j+self.height)
            # Move down by `self.height`.
            for block in Tetris.entities["piece"]:
                a, b = block.coords
                block.set_position(a, b+self.height)
    
    class FallenBlocks:
        """ The structure formed by the fallen piece's `Block`s. """

        height = 0  # Not the same as `Piece.height`.
        
        def grow(self):
            """ Making `Piece` part of the structure. """

            # Remove the `Block`s from the `"piece"` container and add
            # them to the `"fallen"` container.
            Tetris.entities["fallen"].extend(Tetris.entities["piece"])
            for block in Tetris.entities["piece"]:
                block._tags = "fallen"
            Tetris.entities["piece"] = []
            Tetris.canvas.addtag_withtag("fallen", "piece")
            Tetris.canvas.dtag("piece", "piece")

            # Update the structure's height.
            self.height = 20 - min([20] + [block.coords[1]
                                           for block in Tetris.entities["fallen"]])
        
        def remove_full_lines(self):
            full_lines = []
            # Group all the completed lines (with 10 aligned `Block`s)
            # into `full_lines`.
            for b in range(20):
                line = [block
                        for block in Tetris.entities["fallen"]
                        if block.coords[1] == b]
                if len(line) == 10:
                    full_lines.append((b, line))
            # Remove them from the structure and fell the `Block`s
            # above it.
            for b, line in full_lines:
                for block in line:
                    Tetris.canvas.delete(*block.ids)
                    Tetris.entities["fallen"].remove(block)
                    
                for block in Tetris.entities["fallen"]:
                    i, j = block.coords
                    if j < b:
                        block.set_position(i, j+1)
            
            return len(full_lines)  # Used for scoring.


class Client(BaseClient):
    """
    A client for :class:`Tetris`.

    Attributes
    ----------
    window : tk.Tk
        A `tkinter.Tk <https://tkdocs.com/pyref/tk.html>`_ object.
    canvas : tk.Canvas
        A `tkinter.Canvas <https://tkdocs.com/pyref/canvas.html>`_ object.
    """

    def __init__(self):
        """ Initializing the GUI. """

        super().__init__()
        self.window.title("Tetris Game")

        # Load the necessary screens.
        self.screen = Screen(Client)
        self.screen.load_image("victory_screen", "vs")
        self.screen.load_image("defeat_screen", "ds")
        self.screen.load_image("background", "bg")

        # Initialize the game.
        self.game = Tetris(Client)

    def loop(self):
        """ List of scheduled events. """

        # Update `Block`'s mechanics.
        self.game.update_entities(t=self.ticks)

        # Implement the game mechanics and check for endgame.
        self.game.manage(self.ticks)

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

        self.game.handle_events(key, press)


def main():
    """ Output-generating commands. """

    print("Check `", game_manuals, "` for instructions.", sep="")
    client = Client()
    client.start()


if __name__ == '__main__':
    main()
