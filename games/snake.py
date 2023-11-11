""" This module contains an implementation of a Snake game. """

import random
from ..constants import *
from ..client import BaseClient, Screen
from ..block import Block, BlinkingBlock
from . import game_manuals
from .game_engine import Game

__doc__ = "".join([__doc__, "\n\nCheck `", game_manuals, "` for instructions."])
__all__ = ["Snake"]


class Snake(Game):
    """
    Implements `Game` with a snake game.
    
    Attributes
    ----------
    canvas : tkinter.Canvas
        The current `Canvas`.
    direction : str
        Where the snake should turn to.
    growing : bool
        Whether the snake should grow one block after eating.
    entities : dict
        Containers for the objects to be drawn (tag:list).
    """

    direction = "down"
    growing = False
    entities = {"body": [], "food": []}
    
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
        self.speed = 10
        self.key_enabled = False
        """ Allows only one directional movement at a time. """

        # Spawn the entities.
        self.snake = self.Body()
        self.food = self.Food()

        # Identify this game's objects with a tag.
        self.add_tags()

    def reset(self):
        """ Remove all elements from the screen and start again. """

        Snake.direction = "down"
        Snake.growing = False
        super().reset()
    
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
                if key == "space" and self.last_key != "space":
                    self.speed *= 2
                # Lock direction changes after the first until the next
                # iteration.
                elif self.key_enabled:
                    self.key_enabled = False
                    # Direction changes, making sure the snake's head won't
                    # enter itself.
                    if key == "up" and self.direction != "down":
                        Snake.direction = "up"
                    elif key == "down" and self.direction != "up":
                        Snake.direction = "down"
                    elif key == "left" and self.direction != "right":
                        Snake.direction = "left"
                    elif key == "right" and self.direction != "left":
                        Snake.direction = "right"
                self.last_key = key

            else:  # Key released.
                if key == "space":
                    self.speed /= 2
                self.last_key = ""
    
    def manage(self, t):
        """
        Game logic implementation.

        Parameters
        ----------
        t : int
            A timer.
        """

        if self.running and not self.paused:
            self.check_eat()
            # Set the action rate at `speed` blocks per second.
            if t % int(FPS/self.speed) == 0:
                self.update_score()
                self.snake.move()
                self.key_enabled = True
        
        super().manage()  # Manage endgame.
    
    def check_eat(self):
        """ The snake grows if it reaches the food. """

        if self.snake.head.coords == self.food.coords:
            Snake.growing = True
            self.food.respawn()
            # Avoid the food spawning inside the snake.
            while self.food.coords in self.snake.coords:
                self.food.respawn()
    
    def update_score(self):
        """ Scoring mechanics. """

        n = len(Snake.entities["body"])
        if self.growing:
            if 3 < n <= 25:
                self.score += 15
            elif 25 < n <= 50:
                self.score += 45
            elif 50 < n <= 100:
                self.score += 100
            elif 100 < n < 200:
                self.score += 250
        super().update_score()
    
    def check_victory(self):
        """
        Victory occurs when the snake's size becomes the whole grid.

        Returns
        -------
        bool
            Whether the game has been beaten.
        """

        n = len(Snake.entities["body"])
        if n == 200:
            return True
        else:
            return False
    
    def check_defeat(self):
        """
        Defeat happens if the snake's head hits its body or the borders.

        Returns
        -------
        bool
            Whether the game was lost.
        """

        i, j = self.snake.head.coords
        if ((0 <= i < 10) and
                (0 <= j < 20) and
                (i, j) not in self.snake.coords[1:]):
            return False
        else:
            return True
    
    class Body:
        """ Organizes the snake's drawing, movement, and growth. """
        
        def __init__(self):
            # Set the snake's initial position.
            self.coords = [(4, 5), (4, 4), (4, 3)]

            # Add its `Block`s to the container for drawing.
            Snake.entities["body"] = [
                Block(i, j, Snake.source, tags="body")
                for (i, j) in self.coords
            ]

            # Identify the head and the tail.
            self.head = Snake.entities["body"][0]
            self.tail = Snake.entities["body"][-1]
        
        def move(self):
            """ Handle the snake's movement and growth mechanics. """

            # Movement is achieved by creating a new `Block` object in
            # the head's next position, ...
            i, j = CONVERT[Snake.direction]
            a, b = self.head.coords
            self.head = Block(i+a, j+b, Snake.source, tags="body")
            Snake.entities["body"].insert(0, self.head)
            # ... keeping the tail in the same place if the head doesn't
            # hit the food, ...
            if Snake.growing:
                Snake.growing = False
            else:
                # ... or deleting it (references and drawing) otherwise.
                Snake.entities["body"].pop()
                Snake.canvas.delete(*self.tail.ids)
                self.tail = Snake.entities["body"][-1]

            # Update the list of coordinates.
            self.coords = [segment.coords
                           for segment in Snake.entities["body"]]
    
    class Food(BlinkingBlock):
        """ Organizes the food's spawn randomly. """
        
        def __init__(self):
            """ Generate random coordinates to spawn a `BlinkingBlock` at. """

            i = random.randint(0, 9)
            j = random.randint(0, 19)
            super().__init__(i, j, Snake.source, tags="food")
            # Add the instance to the container for drawing.
            Snake.entities["food"] = [self]
        
        def respawn(self):
            """ Generate new random coordinates to move the `BlinkingBlock` to. """

            i = random.randint(0, 9)
            j = random.randint(0, 19)
            self.set_position(i, j)


class Client(BaseClient):
    """
    A client for :class:`Snake`.

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
        self.window.title("Snake Game")

        # Load the necessary screens.
        self.screen = Screen(Client)
        self.screen.load_image("victory_screen", "vs")
        self.screen.load_image("defeat_screen", "ds")
        self.screen.load_image("background", "bg")

        # Initialize the game.
        self.game = Snake(Client)

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
