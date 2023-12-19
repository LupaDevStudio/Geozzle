"""
Module to create the home screen.
"""

###############
### Imports ###
###############

from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    USER_DATA,
    THEMES_DICT
)
from tools.kivy_tools import ImprovedScreen


#############
### Class ###
#############


class GameSummaryScreen(ImprovedScreen):

    def __init__(self, **kwargs) -> None:
        current_background_theme = USER_DATA.settings["current_background_theme"]
        super().__init__(
            back_image_path=PATH_BACKGROUNDS +
            THEMES_DICT[current_background_theme]["image"],
            **kwargs)
