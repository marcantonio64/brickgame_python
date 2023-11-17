""" This module contains an implementation of an Asteroids game. """

import random
from ..constants import *
from ..client import BaseClient, Screen
from ..block import Block, Bomb
from . import game_manuals
from .game_engine import Game

__doc__ = "".join([__doc__, "\n\nCheck `", game_manuals, "` for instructions."])
__all__ = ["Asteroids"]

USE_BOMBS = True


class Asteroids(Game):
    """
    Implements `Game` with an Asteroids game.

    Attributes
    ----------
    canvas : tkinter.Canvas
        The current `Canvas`.
    shooter_speed : int
        Number of bullets per second.
    entities : dict
        Containers for the objects to be drawn (tag:list).
    """

    shooter_speed = 10
    entities = {"asteroids": [],
                "bullet": [],
                "shooter": [],
                "bomb": [],
                }
    
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
        self.asteroids_speed = 2  # Falling speed.
        self.speed = self.asteroids_speed
        self.shooter_mvspeed = 10
        self.game_ticks = 0  # Internal timer for the game.

        # Spawn the entities.
        self.shooter = self.Shooter()  # Also spawns the bullets.
        # Initialize `self.bomb` with a dummy `Bomb` outside the grid.
        self.bomb = Bomb(-5, -5, Asteroids.source)

        # Identify this game's objects with a tag.
        self.add_tags()
    
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
                # Set `Shooter`'s movement.
                if key == "left":
                    self.Shooter.direction = "left"
                elif key == "right":
                    self.Shooter.direction = "right"

            else:  # Key released.
                if key == "left":
                    self.Shooter.direction = ""
                elif key == "right":
                    self.Shooter.direction = ""
    
    def manage(self, t):
        """
        Game logic implementation.

        Parameters
        ----------
        t : int
            A timer.
        """

        if self.running and not self.paused:
            # Separate from the Client's timer for proper scaling of
            # difficulty.
            self.game_ticks += 1

            # Manage multiple simultaneous hits and scoring.
            number_of_collisions = self.check_hit()
            self.update_score(number_of_collisions)
            
            # Set the events with an action rate of `asteroids_speed`
            # `Block`s per second.
            if t % int(FPS/self.asteroids_speed) == 0:
                self.move_asteroids(self.game_ticks)
                self.bomb.move("up")
                self.bomb.check_explosion(
                    target=Asteroids.entities["asteroids"]
                )

            # Set the events with an action rate of `shooter_speed`
            # `Block`s per second.
            if t % int(FPS/self.shooter_speed) == 0:
                # The `Bullet`'s movement is handled by its `update`
                # method.
                self.shooter.shoot()
                self.try_spawn_bomb(self.game_ticks)
        
            if t % int(FPS/self.shooter_mvspeed) == 0:
                self.shooter.move()

        super().manage()  # Manage endgame.

    def check_hit(self):
        """
        Bullets disappear and destroy asteroids on collision.

        Returns
        -------
        int
            Number of asteroid `Block`s destroyed.
        """

        asteroids = Asteroids.entities["asteroids"]
        bullets = Asteroids.entities["bullet"]
        collisions = []
        for bullet in bullets:
            i, j = bullet.coords
            new_collisions = []
            for block in asteroids:
                # A collision happens if the coordinates coincide.
                if block.coords in [(i, j), (i, j+1)]:
                    new_collisions.append(block)
            if new_collisions:
                # Destroy bullet.
                self.canvas.delete(*bullet.ids)
                Asteroids.entities["bullet"].remove(bullet)
            collisions.extend(new_collisions)
        for block in collisions:
            # Destroy asteroids.
            self.canvas.delete(*block.ids)
            Asteroids.entities["asteroids"].remove(block)

        return len(collisions)

    def update_score(self, blocks_hit):
        """ Scoring mechanics. """

        self.score += 5*blocks_hit
        super().update_score()

    def try_spawn_bomb(self, t):
        """
        Handle the `Bomb`'s spawn over time according to its spawn rate.

        Parameters
        ----------
        t : int
            The timer.
        """
        
        # The chance of a `Bomb` spawning increases from 0.1% up to
        # 0.15% after 3 minutes.
        spawn_rate = 1/3000
        if t <= 180*FPS and t % 60*FPS == 0:
            spawn_rate += 1/6000
        (spawning,) = random.choices(
            (USE_BOMBS, False),  # No spawns if `USE_BOMBS` is False.
            (spawn_rate, 1-spawn_rate),
        )
        # It shall spawn at the bottom of the grid with a random
        # horizontal coordinate.
        if spawning:
            i = random.randint(0, 6)
            self.bomb = Bomb(i,
                             19,
                             Asteroids.source,
                             group=Asteroids.entities["bomb"],
                             tags="bomb")
    
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
        Defeat condition.

        Occurs when an ``aster`` `Block` reaches either the ``shooter``
        or the lower border of the grid.

        Returns
        -------
        bool
            Whether the game was lost.
        """

        asteroids = Asteroids.entities["asteroids"]
        shooter, = Asteroids.entities["shooter"]
        # Check for collisions with the `shooter`.
        collision = [block for block in asteroids if block.coords == shooter.coords]
        # Track the asteroids' height.
        distance = max([1] + [asteroid.coords[1] for asteroid in asteroids])
        
        if collision:
            return True
        elif distance >= 20:  # Hitting the bottom.
            return True
        else:
            return False

    def move_asteroids(self, t):
        """
        Organizes the asteroids to be destroyed.

        Manages the spawning and the drawing of the asteroid `Block`s,
        as well as their movement.

        Parameters
        ----------
        t : int
            The timer.
        """

        for asteroid in Asteroids.entities["asteroids"]:
            i, j = asteroid.coords
            asteroid.set_position(i, j+1)

        # Spawn rate starts at 0.3 per tick, increasing linearly up to
        # 0.45 per tick after 3 minutes. (0.5+ is unbeatable.)
        if t < 180*FPS:
            r = 0.3 + t*0.15/(180*FPS)
        else:
            r = 0.45
        choices = random.choices((1, 0), (r, 1-r), k=10)
        for i, choice in enumerate(choices):
            if choice:
                Asteroids.entities["asteroids"].append(
                    Block(i, 0, Asteroids.source, tags="asteroids")
                )

    class Bullet(Block):
        """ A `Block` sprite that moves up. """

        def __init__(self, i, j):
            super().__init__(i,
                             j,
                             Asteroids.source,
                             direction="up",
                             tags="bullet")
            Asteroids.entities["bullet"].append(self)
        
        def update(self, speed, **kwargs):
            """
            Adapt the `Block.update` method for `Bullet`.

            Parameters
            ----------
            speed : int
                A placeholder for the standard parameters, meant
                to be overridden with ``FPS``.
            """

            # The bullet disappears if it hits the top border.
            if self.coords[1] < 0:
                self.canvas.delete(*self.ids)
                Asteroids.entities["bullet"].remove(self)
            # And moves at the update rate speed.
            super().update(speed=FPS, **kwargs)
            
    class Shooter(Block):
        """
        Manages the player-controlled shooter.

        A `Block` sprite moving horizontally at the bottom of the grid
        that can shoot `Bullet`s.

        Attributes
        ----------
        direction : str
            Where to move: ``"left"`` or ``"right"``.
        """

        direction = ""
        
        def __init__(self):
            """ Set `Shooter`'s initial position """

            super().__init__(4, 19, Asteroids.source, tags="shooter")
            Asteroids.entities["shooter"] = [self]
        
        def move(self):
            """ Avoid the shooter from leaving the grid. """

            i, j = self.coords
            a, _ = CONVERT[Asteroids.Shooter.direction]
            if 0 <= i + a < 10:
                self.set_position(i + a, j)
        
        def shoot(self):
            """ Spawn the `Bullet` from the `Shooter`. """

            Asteroids.Bullet(*self.coords)
        
        def update(self, speed, **kwargs):
            """
            Adapt the `Block.update` method for `Shooter`.

            Parameters
            ----------
            speed : int
                A placeholder for the standard parameters, meant
                to be overridden with ``Asteroids.shooter_speed``.
            """

            super().update(speed=Asteroids.shooter_speed, **kwargs)


class Client(BaseClient):
    """
    A client for :class:`Asteroids`.

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
        self.window.title("Asteroids Game")

        # Load the necessary screens.
        self.screen = Screen(Client)
        self.screen.load_image("victory_screen", "vs")
        self.screen.load_image("defeat_screen", "ds")
        self.screen.load_image("background", "bg")

        # Initialize the game.
        self.game = Asteroids(Client)

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
