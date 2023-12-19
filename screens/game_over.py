"""
Module to create the home screen.
"""

###############
### Imports ###
###############

from tools.path import (
    PATH_BACKGROUNDS
)
from tools.kivy_tools import ImprovedScreen


#############
### Class ###
#############


class GameOverScreen(ImprovedScreen):

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "lake_sunset.jpg",
            **kwargs)
