""" Testing `block.py` elements. """

from ..constants import FPS
from ..client import BaseClient
from ..block import *


class Client(BaseClient):
    """
    A functioning client with some tests for `Block` and its derivatives.

    Test targets:

    1. `Block` display
    2. `BlinkingBlock` display and behavior
    3. `Bomb` display and its methods
    4. `set_position()` for `Block` and `BlinkingBlock`
    """

    def __init__(self):
        """ Initializing the tested objects and their containers. """

        # GUI initialization.
        super().__init__()
        self.window.title("Block test")

        # Create tags and groups.
        self.entities = {"first_tag": [],   # tag : group
                         "second_tag": [],
                         "third_tag": [],
                         "fourth_tag": [],
                         }

        # First test's target: static `Block`s.
        self.coords = [(3, 3), (3, 2)]
        self.block_ids = []  # Holds references.
        for (i, j) in self.coords:
            block = Block(i, j, Client, tags="first_tag")
            self.entities["first_tag"].append(block)
            self.block_ids.append(block.ids)

        # Second test's target: static `BlinkingBlock`.
        self.entities["second_tag"].append(BlinkingBlock(7,
                                                         7,
                                                         Client,
                                                         tags="second_tag"))
        #co = [(7,7),(7,6),(7,5),(7,8),(4,12)]
        #for (i, j) in co:
        #    self.entities["second_tag"].append(BlinkingBlock(i,
        #                                                     j,
        #                                                     Client,
        #                                                     tags="second_tag"))

        # Third test's target: `Bomb`.
        self.bomb = Bomb(5,
                         15,
                         Client,
                         group=self.entities["third_tag"],
                         tags="third_tag")

        # Fourth test target: `set_position()` method for `Block` and
        # `BlinkingBlock`
        self.b1 = Block(0, 0, Client, tags="fourth-tag")
        self.b2 = BlinkingBlock(9, 19, Client, tags="fourth-tag")
        self.entities["fourth_tag"] = [self.b1, self.b2]

    def loop(self):
        """ List of scheduled events. """

        if self.ticks > 5*FPS:  # After 5 seconds, do...

            # Test movement for `Snake`: move down two `Block`s.
            i, j = self.coords[0]
            # Draw a third `Block` below and store its data.
            block = Block(i, j+1, Client, tags="first_tag")
            self.entities["first_tag"].insert(0, block)
            self.coords.insert(0, (i, j+1))
            self.block_ids.insert(0, block.ids)
            # Delete the first `Block`'s drawing and data, creating an
            # illusion of movement.
            self.canvas.delete(*self.block_ids[-1])
            self.entities["first_tag"].pop()
            self.block_ids.pop()
            self.coords.pop()

            # Test `BlinkingBlock`'s blinking: by visual checking
            # and tracking its ids' behavior over 5 seconds.
            #if self.ticks <= 10*FPS:
            #    blink, = self.entities["second_tag"]
            #    print(blink.ids, blink.shade.ids)

            # Test `Bomb`'s methods.
            # Change for `"down"` to test the `Bomb`'s behavior when it
            # reaches the bottom of the grid. Quote all occurrences of
            # `"second_tag"` to test for the top instead.
            self.bomb.move("up")
            self.bomb.check_explosion(target=self.entities["second_tag"])

            # Test `.set_position()`
            i, j = self.b1.coords
            self.b1.set_position(i+1, j+1)
            if self.ticks % (2*FPS) == 0:
                i, j = self.b2.coords
                self.b2.set_position(i-1, j-1)

        # Update the `Block`'s mechanics.
        for entity in self.entities.values():
            for block in entity:
                block.update(t=self.ticks, speed=1)

        # Schedule the next iteration.
        super().loop()


def main():
    """ Output-generating commands. """

    client = Client()
    client.start()


if __name__ == '__main__':
    main()
