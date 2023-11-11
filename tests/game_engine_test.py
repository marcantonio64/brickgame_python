""" Testing `game_engine.py` elements. """

import random
from ..constants import FPS
from ..client import BaseClient, Screen
from ..block import *
from ..games.game_engine import *


class NewGame(Game):
    """ Implementing some basic mechanics. """

    entities = {"block": [], "blink": [], "bomb": []}

    def __init__(self, source):
        super().__init__(source)
        # Spawning a `Block` at (3, 3) that moves down.
        self.entities["block"].append(
            Block(3,
                  3,
                  source,
                  direction="down",
                  tags="block")
        )
        # Spawning a `BlinkingBlock` at a random position.
        i = random.randint(0, 9)
        j = random.randint(0, 19)
        self.entities["blink"].append(
            BlinkingBlock(i,
                          j,
                          source,
                          tags="blink")
        )
        # Spawning a `Bomb` at (5, 10).
        Bomb(5,
             10,
             source,
             group=self.entities["bomb"],
             tags="bomb")

    def handle_events(self, key, press):
        super().handle_events(key, press)

    def manage(self):
        super().manage()

    def update_score(self):
        super().update_score()

    def check_victory(self):
        super().check_victory()

    def check_defeat(self):
        super().check_defeat()


class Client(BaseClient):
    """ A functioning client with some tests for `Game`. """

    def __init__(self):
        """ Initializing the tested objects and their containers. """

        super().__init__()
        self.window.title("Game test")

        # Load the necessary screens.
        self.screen = Screen(Client)
        self.screen.load_image("victory_screen", "vs")
        self.screen.load_image("defeat_screen", "ds")
        self.screen.load_image("background", "bg")

        # Initialize the game.
        self.game = NewGame(Client)

    def loop(self):
        """ List of scheduled events. """

        # Update `Block`'s mechanics.
        self.game.update_entities(t=self.ticks)

        # Implement the game mechanics and check for endgame.
        self.game.manage()

        if self.ticks == FPS*10:    # 10 seconds mark.
            self.game.toggle_defeat()
        elif self.ticks == 15*FPS:  # 15 seconds mark.
            self.game.toggle_victory()
        elif self.ticks == 20*FPS:  # 20 seconds mark.
            self.game.reset()

    def handle_events(self, key, press):
        self.game.handle_events(key, press)


def main():
    """ Output-generating commands. """

    client = Client()
    client.start()


if __name__ == '__main__':
    main()
