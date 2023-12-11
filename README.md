# Brick Game with [tkinter](https://docs.python.org/3/library/tkinter.html)

## Overview
An exercise project for GUIs using tools from the [**Python3**](https://www.python.org/)
built-in library [**tkinter**](https://docs.python.org/3/library/tkinter.html).
The goal is to make a client with some simple games: snake, breakout,
asteroids, and tetris.

> Minimum python version: 3.6. 

The aspect is of a 20x10 grid of `Block` objects, which are used
as pixels for the construction of each game.

> A `Block` is drawn to a `tkinter.Canvas` object as an outer
empty square containing a smaller filled square.

A manual with the rules and controls of each game can be found on
`...\brickgame_tkinter\docs\game_manuals.md`. Instructions for adding more games can
be seen on `...\brickgame_tkinter\docs\user_guide.md`.

## Installation
In the command line, after setting up your directory, download the project with:

```shell
git clone https://github.com/marcantonio64/brickgame_tkinter.git
python setup.py install
```

Then run the game package with:

```shell
python -m brickgame_tkinter
```

If you want to play a specific game directly, simply add `.games.` and
the name of the game in lowercase. For example:

```shell
python -m brickgame_tkinter.games.tetris
```

## Inspirations
Bro Code's YouTube video: [Python Full Course for free 🐍](https://www.youtube.com/watch?v=XKHEtdqhLK8&t=41185s).

## Metadata
Author: marcantonio64

Contact: mafigueiredo08@gmail.com

Date: 11-Nov-2023

License: MIT