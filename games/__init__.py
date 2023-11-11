import os
from ..client import package_dir

high_scores_dir = os.path.join(
    package_dir,
    "high-scores.json"
)
""" Directory of `high-scores.json`. """
game_manuals = os.path.join(
    package_dir,
    "docs",
    "game_manuals.md"
)
""" Directory of `game_manuals.md`. """
