""" Establishing the structure, appearance, and behavior of unit cells. """

from .constants import *
from .client import AbsentWindowOrCanvasError, has_window_and_canvas

__all__ = ["Block", "BlinkingBlock", "Bomb"]


class Block:
    """ Unitary cell, colored ``LINE_COLOR`` when active. """

    def __init__(self, i, j, source, color=LINE_COLOR, direction="", tags=""):
        """
        Constructor for :class:`Block` instances.

        Set instance variables, extract ``canvas`` from ``source``, and
        draw squares on it.

        Parameters
        ----------
        i : int
            Horizontal position on the grid.
        j : int
            Vertical position on the grid.
        source : Type[Client]
            A class with ``window`` and ``canvas`` attributes.
        color : str, optional
            Color value. Defaults to ``LINE_VALUE`` (std. black).
        direction : str, optional
            One of ``"up"``, ``"down"``, ``"left"``, or ``"right"``.
        tags : str, optional
            Grouping id for tkinter objects. Defaults to ``""``.

        Raises
        ------
        AbsentWindowOrCanvasError
            If the ``source`` parameter has incorrect ``window`` or ``canvas`` attributes.
        """

        # Check for correct `source`.
        if not has_window_and_canvas(source):
            raise AbsentWindowOrCanvasError("source")

        # Set the instance variables.
        self.canvas = source.canvas   # Extract `canvas`.
        self._color = color
        self._direction = direction
        self._tags = tags
        self.displacement = (0, 0)
        """        
        A 2D-vector of integers.

        Represents the real displacement a :class:`Block` will suffer in
        the next update. It depends on the current game's resolution.
        """
        self.coords = (i, j)
        self.ids = self.draw_at(i, j)  # Draw the squares.

        # Set `Block` in movement.
        self.set_direction(self._direction)

    def update(self, t=0, speed=0):
        """
        Update the inner :class:`Block` mechanics.

        Parameters
        ----------
        t : int, optional
            A timer. Defaults to 0.
        speed : int, optional
            Number of moves per second. Defaults to 0.
        """

        # The `Block` moves only when a direction and a positive speed
        # are specified.
        if self._direction and speed > 0:
            if t % int(FPS/speed) == 0:  # `speed` actions per second.
                out, inn = self.ids
                # Move squares by `displacement`.
                self.canvas.move(out, *self.displacement)
                self.canvas.move(inn, *self.displacement)
                # Adjust the coordinates.
                i, j = self.coords
                a, b = self.displacement
                a /= DIST_BLOCKS
                b /= DIST_BLOCKS
                self.coords = (i+int(a), j+int(b))

    def draw_at(self, i, j):
        """
        Draw squares at the ``canvas`` attribute.

        Parameters
        ----------
        i : int
            Horizontal position on the grid.
        j : int
            Vertical position on the grid.

        Returns
        -------
        tuple[int, int]
            A pair of tkinter ids.
        """

        # Outer square.
        side = PIXEL_SIDE*9
        square = (SIZE_CORRECTION + BORDER_WIDTH + PIXEL_SIDE + DIST_BLOCKS*i,
                  SIZE_CORRECTION + BORDER_WIDTH + PIXEL_SIDE + DIST_BLOCKS*j,
                  SIZE_CORRECTION + BORDER_WIDTH + PIXEL_SIDE + side + DIST_BLOCKS*i,
                  SIZE_CORRECTION + BORDER_WIDTH + PIXEL_SIDE + side + DIST_BLOCKS*j)
        outer_id = self.canvas.create_rectangle(*square,
                                                width=PIXEL_SIDE,
                                                outline=self._color,
                                                tags=self._tags)
        # Inner square.
        side = PIXEL_SIDE*5
        square = (SIZE_CORRECTION + BORDER_WIDTH + PIXEL_SIDE*3 + DIST_BLOCKS*i,
                  SIZE_CORRECTION + BORDER_WIDTH + PIXEL_SIDE*3 + DIST_BLOCKS*j,
                  SIZE_CORRECTION + BORDER_WIDTH + PIXEL_SIDE*3 + side + DIST_BLOCKS*i,
                  SIZE_CORRECTION + BORDER_WIDTH + PIXEL_SIDE*3 + side + DIST_BLOCKS*j)
        inner_id = self.canvas.create_rectangle(*square,
                                                fill=self._color,
                                                width=PIXEL_SIDE,
                                                outline=self._color,
                                                tags=self._tags)
        return outer_id, inner_id

    def set_position(self, i, j):
        """
        Move :class:`Block` to the specified position.

        Parameters
        ----------
        i : int
            New horizontal position on the grid.
        j : int
            New vertical position on the grid.
        """

        self.canvas.delete(*self.ids)  # Erase the previous drawing.
        self.ids = self.draw_at(i, j)  # Draw anew and store the data.
        self.coords = (i, j)

    def set_direction(self, direction):
        """
        Update the ``displacement`` attribute to move the :class:`Block`
        according to the ``direction`` parameter.

        Parameters
        ----------
        direction : str
            One of ``"up"``, ``"down"``, ``"left"``, or ``"right"``.
        """

        if direction:
            i, j = CONVERT[direction]
            x = i*DIST_BLOCKS
            y = j*DIST_BLOCKS
            self._direction = direction
            self.displacement = (x, y)


class BlinkingBlock(Block):
    """ Just a :class:`Block` with its color alternating with a shade. """

    def __init__(self, i, j, source, tags=""):
        """
        Constructor for :class:`BlinkingBlock` instances.

        Draw a normal :class:`Block` and a *shaded* :class:`Block`, which will be
        set to alternate over time (twice per second).

        Parameters
        ----------
        i : int
            Horizontal position on the grid.
        j : int
            Vertical position on the grid.
        source : Type[Client]
            A class with ``window`` and ``canvas`` attributes.
        tags : str, optional
            Grouping id for tkinter objects. Defaults to ``""``.

        Raises
        ------
        AbsentWindowOrCanvasError
            If the ``source`` parameter has incorrect ``window`` or ``canvas`` attributes.
        """

        self._active = True  # Always spawns 'on'.

        # Draw a block with `SHADE_COLOR`, which has a lighter tone
        # than `LINE_COLOR`.
        self.shade = Block(i, j, source, color=SHADE_COLOR, tags=tags)
        # Draw a block with `LINE_COLOR` (standard `color` parameter).
        super().__init__(i, j, source, tags=tags)

    def update(self, t=0, speed=0):
        """
        Update the inner :class:`BlinkingBlock` mechanics.

        Parameters
        ----------
        t : int, optional
            A timer. Defaults to 0.
        speed : int, optional
            Number of moves per second. Defaults to 0.
        """

        if t > 0:
            if t % FPS == 0:
                # Draw the `Block` with `LINE_COLOR`.
                [self.canvas.tag_raise(id) for id in self.ids]
                self._active = True
            elif t % FPS == int(FPS / 2):
                # Draw the `Block` with `SHADE_COLOR`.
                [self.canvas.tag_raise(id) for id in self.shade.ids]
                self._active = False

        # Adding `Block.update()` calls to allow movement.
        self.shade.update(t, speed)
        super().update(t, speed)

    def set_position(self, i, j):
        """
        Move :class:`BlinkingBlock` to the specified position.

        Parameters
        ----------
        i : int
            New horizontal position on the grid.
        j : int
            New vertical position on the grid.
        """

        # Ensuring the `BlinkingBlock` maintains its state when
        # moved (the last drawing becomes top level in tkinter).
        if self._active:
            self.shade.set_position(i, j)
            super().set_position(i, j)
        else:
            super().set_position(i, j)
            self.shade.set_position(i, j)

    def set_direction(self, direction):
        """
        Update the ``displacement`` attribute to move the
        :class:`BlinkingBlock` according to ``direction``.

        Parameters
        ----------
        direction : str
            One of ``"up"``, ``"down"``, ``"left"``, or ``"right"``.
        """

        self.shade.set_direction(direction)
        super().set_direction(direction)


class Bomb:
    """
    Used to destroy blocks from a target upon collision.

    Made with a group of :class:`Block` and :class:`BlinkingBlock`
    objects in an *X* shape, akin to a sea mine.
    """

    _bombs = []  # List of active `Bomb`s, shared within the objects.

    def __init__(self, i, j, source, group=None, tags=""):
        """
        Constructor for :class:`Bomb` instances.

        Instantiate the required :class:`Block` and :class:`BlinkingBlock`
        objects and organize them according to ``group`` and ``tags``.

        Parameters
        ----------
        i : int
            Horizontal position of the top left corner.
        j : int
            Vertical position of the top left corner.
        source : Type[Client]
            A class with a ``window`` and a ``canvas`` attributes.
        group : list, optional
            Tracking group for the :class:`Bomb`'s elements. Defaults to ``[]``.
        tags : str, optional
            Grouping id for tkinter objects. Defaults to ``""``.

        Raises
        ------
        AbsentWindowOrCanvasError
            If the ``source`` parameter has incorrect ``window`` or ``canvas`` attributes.
        """

        if not has_window_and_canvas(source):
            raise AbsentWindowOrCanvasError
        if group is None:
            group = []
        self._canvas = source.canvas  # Extract `canvas`.
        self._group = group
        if tags:
            # `Bomb` construction:
            bomb = [
                # 4 outer corners with `BlinkingBlock`s.
                BlinkingBlock(i, j, source, tags=tags),
                BlinkingBlock(i, j+3, source, tags=tags),
                BlinkingBlock(i+3, j, source, tags=tags),
                BlinkingBlock(i+3, j+3, source, tags=tags),
                # 4 inner `Block`s.
                Block(i+1, j+1, source, tags=tags),
                Block(i+1, j+2, source, tags=tags),
                Block(i+2, j+1, source, tags=tags),
                Block(i+2, j+2, source, tags=tags),
                # Filling the sides with invisible `Block`s.
                Block(i, j+1, source, color=SHADE_COLOR, tags=tags),
                Block(i, j+2, source, color=SHADE_COLOR, tags=tags),
                Block(i+3, j+1, source, color=SHADE_COLOR, tags=tags),
                Block(i+3, j+2, source, color=SHADE_COLOR, tags=tags),
                Block(i+1, j, source, color=SHADE_COLOR, tags=tags),
                Block(i+2, j, source, color=SHADE_COLOR, tags=tags),
                Block(i+1, j+3, source, color=SHADE_COLOR, tags=tags),
                Block(i+2, j+3, source, color=SHADE_COLOR, tags=tags),
            ]
            # Add `bomb`'s components to `_group` for drawing.
            self._group.extend(bomb)
            # Add `bomb` to `Bomb._bombs` for iteration.
            Bomb._bombs.append(bomb)

    def move(self, direction):
        """
        Handle :class:`Bomb` movement.

        Parameters
        ----------
        direction : str
            One of ``"up"``, ``"down"``, ``"left"``, or ``"right"``.
        """

        i, j = CONVERT[direction]
        for bomb in Bomb._bombs[::-1]:
            # Start the movement of each component through
            # `.set_position()`.
            for block in bomb:
                a, b = block.coords
                block.set_position(i+a, j+b)

            # Delete a `Bomb` when it exits the grid.
            _, b = bomb[0].coords
            if (direction == "up" and b < 0  # At the top.
                    or direction == "down" and b >= 17):  # At the bottom.
                for block in bomb:
                    # Erase the drawings.
                    self._canvas.delete(*block.ids)
                    # Remove references.
                    if self._group:
                        self._group.remove(block)
                    if isinstance(block, BlinkingBlock):
                        self._canvas.delete(*block.shade.ids)
                Bomb._bombs.remove(bomb)

    def check_explosion(self, target):
        """
        Manage collision detection.

        Parameters
        ----------
        target : list[Block, BlinkingBlock]
            List of :class:`Block` and :class:`BlinkingBlock` objects to be
            destroyed.

        Returns
        -------
        bool
            Whether any of the bombs hit the target.
        """

        erased_list = []  # Keeping track of which `Bomb`s exploded.

        # Return an empty list if `target` is empty/not iterable.
        if not (target or hasattr(target, "__len__")):
            return []

        # Iterate through `Bomb._bombs` keeping track of the indexes
        # for deletions.
        for bomb_index, bomb in enumerate(Bomb._bombs):
            i, j = bomb[0].coords
            # Detect explosion.
            for block in target:
                a, b = block.coords
                if (i <= a <= i+3) and (j <= b <= j+3):
                    erased_list.append(bomb_index)
                    # Stop if any component of `target` reaches `Bomb`.
                    break
        # Explode.
        for index in erased_list[::-1]:
            self.explode(target, index=index)
        return bool(erased_list)  # If any explosion happened.

    def explode(self, target, index=-1):
        """
        Manage explosion.

        Parameters
        ----------
        target : list[Block, BlinkingBlock]
            List of :class:`Block` and :class:`BlinkingBlock` objects to be
            destroyed.
        index : int
            Index of an exploding member of ``Bomb._bombs``.

        Returns
        -------
        bool
            Whether any of the bombs hit the target.
        """

        # Iterate reversely to keep `erased_list` true to its purpose.
        bomb = Bomb._bombs[index]
        i, j = bomb[0].coords
        targets_hit = []
        # Destroy `target`.
        for block in target:
            a, b = block.coords
            # Blast range of 2 `Blocks` from the `Bomb`'s edges.
            if (i-2 <= a <= i+5) and (j-2 <= b <= j+5):
                # Erase the drawings.
                self._canvas.delete(*block.ids)
                if isinstance(block, BlinkingBlock):
                    self._canvas.delete(*block.shade.ids)
                targets_hit.append(block)
        for hit in targets_hit:
            target.remove(hit)  # Remove references.
        # Destroy `bomb`.
        for block in bomb:
            # Erase the drawings.
            self._canvas.delete(*block.ids)
            # Remove references.
            if block in self._group:
                self._group.remove(block)
            if isinstance(block, BlinkingBlock):
                self._canvas.delete(*block.shade.ids)
        # Remove the references for the exploded bombs.
        del Bomb._bombs[index]

    def init(self, *args, **kwargs):
        self.__init__(*args, **kwargs)
