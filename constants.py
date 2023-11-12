# Colors.
BACK_COLOR = "#6d785c"   # Light green
SHADE_COLOR = "#61705b"  # Dark green
LINE_COLOR = "#000000"   # Black

# Window sizes.
_SCREEN_RES = {"GIGA":   (666, 1326),
               "Huge":   (555, 1105),
               "large":  (444, 884),
               "big":    (333, 663),
               "medium": (222, 442),
               "small":  (111, 221),
               }
"""
Window dimension configs with the correct aspect ratio.

Larger resolutions may require the screen to be viewed 
in portrait mode.
"""
_SIZE = "big"  # Change this to play in other sizes.
_RES = _SCREEN_RES[_SIZE]
WINDOW_WIDTH, WINDOW_HEIGHT = _RES

# Handling directions.
CONVERT = {"down":  (0, 1),
           "up":    (0, -1),
           "right": (1, 0),
           "left":  (-1, 0),
           "":      (0, 0),
           }

# Block dimensions.
WHITE_BORDER = 2  # Dealing with the tkinter's residual white border.
_CORRECTIONS = {"GIGA":  -1,
                "Huge":  -1,
                "large":  0,
                "big":    0,
                "medium": 1,
                "small":  1,
                }
SIZE_CORRECTION = _CORRECTIONS[_SIZE]
PIXEL_SIDE = int(WINDOW_WIDTH/111)
BLOCK_SIDE = PIXEL_SIDE*10
DIST_BLOCKS = BLOCK_SIDE+PIXEL_SIDE
BORDER_WIDTH = int(WINDOW_WIDTH/111)

# Time handling.
TICK_RATE = 16  # Minimum time interval, in milliseconds.
FPS = int(1000/TICK_RATE)  # Approx. 60 when `TICK_RATE` is 16.
