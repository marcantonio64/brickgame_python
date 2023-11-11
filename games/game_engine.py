""" This module contains a base class with general game mechanics. """

import json
from abc import ABC, abstractmethod
from . import high_scores_dir
from ..client import *

__all__ = ["Game"]


class Game(ABC):
    """
    Engine for pixel games in a 10x20 grid.

    Attributes
    ----------
    canvas : tkinter.Canvas
        The current `Canvas`.
    entities : dict
        Container for all `Block` objects and derivatives.
    """

    # Class variables, shared with instances and nested classes.
    canvas = None
    entities = None
    source = None
    
    def __init__(self, source):
        """
        Set instance variables and load images.

        Images are to be loaded to a `Client` object containing this
        class as an attribute, with the tags:

        * ``"bg"`` for background
        * ``"vs"`` for victory_screen
        * ``"ds"`` for defeat_screen

        Parameters
        ----------
        source : Type[Client]
            A class with ``window`` and ``canvas`` attributes.

        Raises
        ------
        AbsentWindowOrCanvasError
            If the ``source`` parameter has incorrect ``window`` or ``canvas`` attributes.
        """

        # Check for correct `source`.
        if not has_window_and_canvas(source):
            raise AbsentWindowOrCanvasError("source")
        Game.source = source

        # Set the instance variables.
        self.score = 0
        self.highest_score = 0
        self.speed = 1  # Unit cells per second.
        self.paused = False
        self.running = True
        """ Whether the game is active. """
        self.name = self.__class__.__name__
        self.last_key = ""
        self.canvas = source.canvas  # Extract `canvas`
        """ Keylock to avoid errors. """

        # Set a class variable that can be shared with nested classes.
        Game.canvas = source.canvas
        """ Current `tkinter.Canvas`. """

        # Show the background.
        self.canvas.tag_raise("bg")

    def reset(self):
        """ Removes all elements from the screen and start again. """

        self.running = True
        # Clean the groups.
        for entity in self.entities:
            self.canvas.delete(entity)
            self.entities[entity] = []
        # Start again.
        self.__init__(Game.source)
    
    @abstractmethod
    def handle_events(self, key, press):
        """
        Deal with user input during a game.

        Parameters
        ----------
        key : str
            Current key.
        press : bool
            Whether the key was pressed or released.
        """

        # Setting *P* for pause/unpause and *Return* for reset.
        if press:
            if key == "p":
                self.paused = not self.paused
                if self.paused:
                    print("Game paused")
                else:
                    print("Game unpaused")
            elif key == "return":
                self.reset()
    
    @abstractmethod
    def manage(self, *args):
        """
        Game logic implementation.

        t : int
            A timer.
        """

        if self.running and not self.paused:
            if self.check_victory():
                self.toggle_victory()
                print("Congratulations!")
                print("Your score on", self.name, ":", self.score)
            if self.check_defeat():
                self.toggle_defeat()
                print("Better luck next time...")
                print("Your score on", self.name, ":", self.score)
    
    @abstractmethod
    def update_score(self, *args):
        """ Communicate with the `high-scores.json` file. """

        # Read the highest score for the current game.
        try:
            with open(high_scores_dir, "r") as file:
                high_scores = json.load(file)
                self.highest_score = high_scores[self.name]
        except Exception as e:
            print(e)
            print("Failed to read 'high-scores.json'.")
            pass  # This interrupts the scoring system without stopping the game.
        
        # Update the highest score to the .json file.
        if self.score > self.highest_score:
            if self.score >= 10**8:
                self.score = 10**8 - 1  # Max value
            else:
                self.highest_score = self.score
            try: 
                with open(high_scores_dir, "w") as file:
                    high_scores[self.name] = self.highest_score
                    json.dump(high_scores, file)
            except Exception as e:
                print(e)
                # print("Failed to update 'high-scores.json'.")
    
    @abstractmethod
    def check_victory(self):
        return False
    
    @abstractmethod
    def check_defeat(self):
        return False
    
    def toggle_victory(self):
        """ Removes all elements from the screen and show victory_screen. """

        self.running = False
        # Clean the groups.
        for entity in self.entities:
            self.canvas.delete(entity)
            self.entities[entity] = []
        # Show the victory message.
        self.canvas.tag_raise("vs")
    
    def toggle_defeat(self):
        """ Removes all elements from the screen and show defeat_screen. """

        self.running = False
        # Clean the groups.
        for entity in self.entities:
            self.canvas.delete(entity)
            self.entities[entity] = []
        # Show the defeat message.
        self.canvas.tag_raise("ds")

    def update_entities(self, **kwargs):
        """ Update `Block`'s mechanics. """

        if not self.paused:
            for entity in self.entities.values():
                for block in entity:
                    block.update(speed=self.speed, **kwargs)
    
    def add_tags(self):
        """ Add an identifier with ``name`` to all game elements. """

        for entity in self.entities:
            self.canvas.addtag_withtag(self.name, entity)
