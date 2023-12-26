"""
Module to create the game over screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    ObjectProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_TEXT_FONT
)
from tools.kivy_tools import ImprovedScreen

#############
### Class ###
#############


class GameOverScreen(ImprovedScreen):

    continent_color = ObjectProperty((1,0,0,1)) # TODO

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "lake_sunset.jpg",
            font_name=PATH_TEXT_FONT,
            **kwargs)

    def go_back_to_home(self):
        self.manager.current = "home"
