""" Entry point for the execution of the main package. """

import os
import json
from . import _screen_generator
from .constants import *
from .client import BaseClient, Screen, screens_dir
from ._screen_generator import show_high_scores
from .games import *
from .games.snake import Snake
from .games.breakout import Breakout
from .games.asteroids import Asteroids
from .games.tetris import Tetris

__all__ = ["Brickgame"]


# List all images with the current resolution:
res_images = [
    img for img in os.listdir(screens_dir) if img.endswith(f"{WINDOW_HEIGHT}.png")
]
# Check if `screens/` exists and has the correct number of images (15)
# for the current resolution.
if not os.path.exists(screens_dir):
    os.mkdir(screens_dir)
    _screen_generator.main()
elif len(res_images) < 15:
    _screen_generator.main()


class Brickgame(BaseClient):
    """
    Manages all the client and game mechanics and their interactions.

    Attributes
    ----------
    window : tk.Tk
        A `tkinter.Tk <https://tkdocs.com/pyref/tk.html>`_ object.
    canvas : tk.Canvas
        A `tkinter.Canvas <https://tkdocs.com/pyref/canvas.html>`_ object.
    environment : str
        The active environment for user input.
    game : Type[Game]
        The current game being played.
    """

    environment = "selector"
    game = None

    def __init__(self):
        """ Initializing the GUI. """

        # Create the .json file, if it doesn't already exist.
        try:
            with open(high_scores_dir, "x") as file:
                json.dump({
                    "Snake": 0,
                    "Breakout": 0,
                    "Asteroids": 0,
                    "Tetris": 0,
                }, file)
            print("File `high-scores.json` successfully created at",
                  package_dir)
        except Exception as e:
            print(e)

        super().__init__()
        self.window.title("Game Selection")

        # Load the necessary screens.
        self.screen = Screen(Brickgame)
        self.screen.load_image("victory_screen", "vs")
        self.screen.load_image("defeat_screen", "ds")
        self.screen.load_image("background", "bg")

        # Render the environments.
        self.selector = self.Selector()

        # Draw the background.
        self.canvas.tag_raise("bg")

    def loop(self):
        """ List of scheduled events. """

        if self.environment == "selector":
            self.selector.animate_screen()
        elif self.environment == "game":
            # Resetting is required for the previews inner loop. 
            self.selector.timer = 0
            # Implement the game mechanics and check for endgame.
            self.game.manage(self.ticks)
            # Update `Block`'s mechanics.
            self.game.update_entities(t=self.ticks)

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

        if self.environment == "selector":
            # Shift to `selector` keybindings.
            self.selector.handle_events(key, press)
        elif self.environment == "game":
            # Leave the `game` instance if *Backspace* is pressed.
            if press and key == "backspace":
                Brickgame.environment = "selector"
                Brickgame.window.title("Game Selection")
            else:
                # Shift to `game` keybindings otherwise.
                self.game.handle_events(key, press)

        self.canvas.update()

    class Selector:
        """ Mechanics for game selection, previews, and high scores. """

        def __init__(self):
            """ Instantiate the game classes and load previews. """

            # The game timers start only when they are selected.
            self.select = {1: Snake(Brickgame),
                           2: Breakout(Brickgame),
                           3: Asteroids(Brickgame),
                           4: Tetris(Brickgame),
                           }
            self.number_of_games = len(self.select)
            self.game_names = [self.select[i+1].__class__.__name__
                               for i in range(self.number_of_games)]
            self.stage_id = 1  # Show `Snake` first.
            self.name = self.game_names[self.stage_id-1]
            self.timer = 0
            self.screen = Screen(Brickgame)

            # Import and load all preview screens.
            self.previews = {}
            for game_name in self.game_names:
                self.previews[game_name] = []
                for i in range(3):
                    tag = "".join([game_name, "_", str(i+1)])
                    self.screen.load_image(tag, tags=tag)
                    Brickgame.canvas.addtag_withtag("preview", tag)

        def handle_events(self, key, press):
            """
            Set game keybindings.

            Parameters
            ----------
            key : str
                Current key.
            press : bool
                Whether the key was pressed or released.
            """

            if press:  # Key press.
                if key == "return":
                    # Entering a game.
                    if self.stage_id <= self.number_of_games:
                        Brickgame.environment = "game"
                        Brickgame.game = self.select[self.stage_id]
                        Brickgame.game.add_tags()
                        self.name = Brickgame.game.__class__.__name__
                        # Update the window title and inform of the
                        # game change.
                        Brickgame.window.title(self.name)
                        print("Now playing:", self.name)
                        # Draw the background and the game elements.
                        Brickgame.canvas.tag_raise("bg")
                        Brickgame.canvas.tag_raise(self.name)
                        # This avoids the need for pressing *Return*
                        # twice after endgames.
                        if not Brickgame.game.running:
                            Brickgame.game.reset()
                # Choosing a game.
                elif key == "left":
                    if self.stage_id > 1:
                        if self.stage_id > self.number_of_games:
                            Brickgame.canvas.delete("high-scores")
                            Brickgame.window.title("Game Selection")
                        self.stage_id -= 1
                        self.name = self.game_names[self.stage_id-1]
                        self.timer = 0
                        self.animate_screen()
                    else:
                        self.stage_id = self.number_of_games+1
                        show_high_scores(Brickgame)
                elif key == "right":
                    if self.stage_id <= self.number_of_games:
                        self.stage_id += 1
                        self.timer = 0
                        self.animate_screen()
                        if self.stage_id > self.number_of_games:
                            show_high_scores(Brickgame)
                        else:
                            self.name = self.game_names[self.stage_id-1]
                    else:
                        self.stage_id = 1
                        self.name = self.game_names[self.stage_id-1]
                        Brickgame.canvas.delete("high-scores")
                        Brickgame.window.title("Game Selection")
                        self.timer = 0
                        self.animate_screen()

        def animate_screen(self):
            """
            Toggle game previews.

            Iterates through each game's previews, with 3 frames per
            second. The previews were built as pixel images, in the
            :mod:`_screen_generator`_ module.
            """

            index = int(3*(self.timer % FPS)/FPS)
            if self.timer % int(FPS/3) == 0:
                # Access the correspondent preview.
                if self.stage_id <= self.number_of_games:
                    Brickgame.canvas.tag_raise(
                        "".join([self.name, "_", str(index+1)])
                    )
            self.timer += 1


def main():
    """ Output-generating commands. """

    print("Check `", game_manuals, "` for instructions.", sep="")
    brickgame = Brickgame()
    brickgame.start()


if __name__ == '__main__':
    main()
