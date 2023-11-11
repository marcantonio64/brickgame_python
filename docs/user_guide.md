# Project User Guide

Instructions on how to expand the project.

## Adding more games/updating

New game modules should be in `...\brickgame_tkinter\games\`. 
The general rules for consistency are:

### Import statements
The general game elements and structures are defined at 
`...\brickgame_tkinter\games\game_engine.py`, and the client's 
definitions pertain to `...\brickgame_tkinter\client.py`.
For each new game, the standard imports are:

```python3
from ..constants import *
from ..client import BaseClient
from ..block import *
from .game_engine import Game
```

You may also import the `random` built-in module, or any of 
your preference.
  
### Class structure
The class containing the new game should implement `Game` and 
be imported to `...\brickgame_tkinter\__main__.py`.
The class may follow this template:

```python3
class NewGame(Game):
    """
    Implements `Game` with a snake game.
    
    Attributes
    ----------
    canvas : tkinter.Canvas
        The current `Canvas`.
    entities : dict
        Containers for the objects to be drawn (tag:list).
    ...
    """
    
    ...
    entities  = {"first_entity": [],
                 "second_entity": [],
                 ...
                }
    ...
    
    def __init__(self, source):
        """
        Initialize instance attributes and instantiate game objects.

        Parameters
        ----------
        source : type[Client]

        Raises
        ------
        AbsentWindowOrCanvasError
            If the ``source`` parameter has o correct `window` or `canvas` attribute.
        """
        
        super().__init__(source)
        
        # Spawn the entities.
        self.first_entity = self.FirstEntity()
        self.second_entity = self.SecondEntity()
        ...
    
    def reset(self):  # Add this if you define extra class variables, like speed
        """ Remove all elements from the screen and start again. """

        # NewGame.newvar1 = ...
        # NewGame.newvar2 = ...
        ...
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

        if press:  # Key pressed.
            # if key == ...:
            #     ...
            ...
            self.last_key = key
        else:      # Key released.
            # if key == ...:
            #     ...
            ...
            self.last_key = ""
    
    def manage(self):
        """ Game logic implementation. """
        
        if self.running and not self.paused:
            # List of events.
            ...
        
        super().manage()  # Manage endgame.
    
    def update_score(self):
        """ Scoring mechanics. """
        
        ...
        super().update_score()
    
    def check_victory(self):
        """
        Victory occurs when "...".

        Returns
        -------
        bool
            Whether the game has been beaten.
        """
        
        if ...:  # Victory condition.
            return True
        else:
            return False
    
    def check_defeat(self):
        """
        Defeat happens if "...".

        Returns
        -------
        bool
            Whether the game was lost.
        """

        if ...:  # Defeat condition.
            return True
        else:
            return False
    
    ...  # Rest of the methods.
    
    class FirstEntity:
        """ docstring """
        
        def __init__(self):
            ...
        
        ... # Rest of the methods.
        
    class SecondEntity:
        """ docstring """
        
        def __init__(self):
            ...
          
        ...  # Rest of the methods.
```
  
### Playing/Testing
To run the game/check for errors, you will need to create an
instance of `Client`, for which you can follow this template:

```python3
class Client(BaseClient):
    """
    A client for :class:`NewGame`.

    Attributes
    ----------
    window : tk.Tk
        A `tkinter.Tk <https://tkdocs.com/pyref/tk.html>`_ object.
    canvas : tk.Canvas
        A `tkinter.Canvas <https://tkdocs.com/pyref/canvas.html>`_ object.
    """

    def __init__(self):
        """ Initializing the GUI. """

        # Initialize the GUI.
        super().__init__()
        self.window.title("NewGame Game")

        # Load the necessary screens.
        self.load_image("victory_screen", "vs")
        self.load_image("defeat_screen", "ds")
        self.load_image("background", "bg")

        # Initialize the game.
        self.game = NewGame(Client)

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
```

After which you can set up the `if __name__ == '__main__'`
statement:

```python3
def main():
    """ Output-generating commands. """

    client = Client()
    client.start()


if __name__ == '__main__':
    main()
```

### Updates in `...\brickgame_tkinter\__main__.py`
Some changes need to be made in order to properly load the game 
when running the full package:
* Import the game into `...\brickgame_tkinter\__main__.py` with 
 `from newgame import NewGame`;
* Update the file `...\brickgame_tkinter\high-scores.json` by 
  changing the `Brickgame.__init__()` constructor, adding 
  `"NewGame": 0,` in `json.dumps()` at the `try` statement (line
  54).
  Before:
  ```python
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
  ```
  After:
  ```python
  # Create the .json file, if it doesn't already exist.
  try: 
      with open(high_scores_dir, "x") as file:
          json.dump({
              "Snake": 0,
              "Breakout": 0,
              "Asteroids": 0,
              "Tetris": 0,
              "NewGame": 0,
          }, file)
      print("File `high-scores.json` successfully created at",
            package_dir)
  except Exception as e:
      print(e)
  ```
* Update the `Brickgame.Selector.__init__()` constructor by 
  adding `n: NewGame(Brickgame),` to `self.select` (line 127) (`n` is
  the new number of games).
    Before:
  ```python
  self.select = {1: Snake(Brickgame),
                 2: Breakout(Brickgame),
                 3: Asteroids(Brickgame),
                 4: Tetris(Brickgame),
                }
  ```
  After:
  ```python
  self.select = {1: Snake(Brickgame),
                 2: Breakout(Brickgame),
                 3: Asteroids(Brickgame),
                 4: Tetris(Brickgame),
                 5: NewGame(Brickgame),
                 }
  ```

### Updates in `...\brickgame_tkinter\_screen_generator.py` 
    and in `...\brickgame_tkinter\screens\`
The image previews for each game are stored in `...\brickgame_tkinter\screens\` 
and the new game's previews can be built using the *screen_generator.py* 
module. You will need to write three new functions in it with 
this format:

```python3
@create_image
def draw_newgame_i(file_name, source):
    """ ith preview for Newgame. """
    
    sketch = { ... }
```

For example:

```python3
@create_image
def draw_tetris_3(file_name, source):
    """ Third preview for Tetris. """
    
    sketch = { 0: (                            ),
               1: (                            ),
               2: (                            ),
               3: (         3, 4, 5,           ),
               4: (            4,              ),
               5: (                            ),
               6: (                            ),
               7: (                            ),
               8: (                            ),
               9: (                            ),
              10: (0,                          ),
              11: (0,                          ),
              12: (0, 1, 2,          6, 7,     ),
              13: (0, 1, 2, 3,    5, 6, 7, 8, 9),
              14: (                            ),
              15: (         3, 4, 5,           ),
              16: (         3,       6,        ),
              17: (         3,       6,        ),
              18: (         3,       6,        ),
              19: (         3, 4, 5,           )}
```

> Remember to add the `ith` letter of the alphabet for identification.

The result previews shall contain 3 new images as 
`...\brickgame_tkinter\screens\newgame_i_wxh.png`, where:
* `i` is the index, from 1 to 3;
* `w` is the current window's width;
* `h` is the current window's height.