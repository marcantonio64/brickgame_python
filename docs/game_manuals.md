# Game Manuals

## Introduction

General instructions and standard controls for the client and for each
game.

After install, start the client by setting your directory and running
the package with:

```shell
python -m brickgame_tkinter
```

Alternatively, run a game directly with, for example:

```shell
python -m brickgame_tkinter.games.tetris
```

## Selector

The client's interface. It is composed of the game previews
(3 looping images), ordered alphabetically with capital letters,
and a High-Scores screen.

The High Scores values are stored in the *high-scores.json* file.
You can reset the values manually or by simply deleting the file before
running the package again.

### Keybindings

Use the directional keys **Left** and **Right** to see the available games
and the High Scores screen.

Press **Return** to start/continue a game.

Once in a game, you can:

* Press **P** to pause/unpause;
* Press **Return** to reset the current game;
* Press **Backspace** to return to the Selector.

> When pressing **Backspace**, the progress in a game **will not be lost**
> until the game ends, is reset, or the window is closed. 

## Snake

A classical snake game. Move the `Snake` to help if reach the
`Food` and grow, avoiding the `Snake` from moving into itself
or exiting the grid.

### Keybindings

Use the directional keys (**Up**/**Down**/**Left**/**Right**) to move the
`Snake`.

Press **Space** to speed up the game if it is not paused.

## Breakout

Control a `Paddle` to deflect a `Ball` and destroy all the `Target`
blocks, while stopping the `Ball` from falling off the grid.

The player can change the `Ball`'s trajectory by dragging it with the
`Paddle` once they meet.

### Keybindings

Use the directional keys **Left** and **Right** to move the `Paddle`.

Press **Space** to:

* Release the ball at the start of each stage;
* Speed up the game at any point if it is not paused.

## Asteroids

Control a `Shooter` to destroy the falling `Asteroids` and stop
them from reaching the bottom of the grid.

A `Bomb` may occasionally appear to help you.

> To deactivate the `Bomb` mechanics, access the module
> `...\brickgame_tkinter\games\asteroids.py` and change the value of
> the constant `USE_BOMBS` to `False`.

### Keybindings

Use the directional keys **Left** and **Right** to move the `Shooter`.

## Tetris

Control the falling `Piece` objects (also known as *tetrominoes*) and
form full lines. If the `Fallen` structure reaches the top of the grid,
**you lose**.

## Keybindings

Use the directional keys **Left** and **Right** to move each falling `Piece`.

**Down** accelerates the fall, and **Space** makes the `Piece` fall instantly.

Press **Right Shift** to switch the current `Piece` with the next preview
(only once for every new `Piece`).