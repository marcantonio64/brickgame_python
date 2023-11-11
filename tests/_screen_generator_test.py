""" Testing `screens/` images. """

from ..constants import FPS
from ..client import BaseClient, Screen
from ..block import *


class Client(BaseClient):
    """ A client with tests for `Screen.load_image()`. """

    def __init__(self):
        super().__init__()
        self.window.title("Screens test")

        self.screen = Screen(Client)
        self.screen.load_image("victory_screen", tags="vs")
        self.screen.load_image("background", tags="bg")
        Block(3, 5, Client)
        self.b = BlinkingBlock(6, 5, Client)
        self.bomb_group = []
        Bomb(3, 10, Client, group=self.bomb_group, tags="b")

    def loop(self):
        self.b.update(self.ticks)
        [block.update(self.ticks) for block in self.bomb_group]
        if self.ticks % (10*FPS) == 0:
            self.canvas.tag_raise("bg")
            print(10)
        elif self.ticks % (5*FPS) == 0:
            self.canvas.tag_lower("bg")
            print(5)
        if self.ticks == (20*FPS):
            self.canvas.tag_raise("vs")
            print(20)


def main():
    """ Output-generating commands. """

    client = Client()
    client.start()


if __name__ == '__main__':
    main()
