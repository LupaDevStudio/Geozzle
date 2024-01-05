"""
Module to create the game over screen.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_TEXT_FONT,
)
from tools.constants import (
    LIST_CONTINENTS,
    DICT_CONTINENTS,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED
)
from tools.kivy_tools import ImprovedScreen

#############
### Class ###
#############


class GameOverScreen(ImprovedScreen):

    code_continent = StringProperty(LIST_CONTINENTS[0])
    continent_color = ColorProperty(DICT_CONTINENTS[LIST_CONTINENTS[0]])
    background_color = ColorProperty(DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[LIST_CONTINENTS[0]])

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "lake_sunset.jpg",
            font_name=PATH_TEXT_FONT,
            **kwargs)

    def update_text(self):
        """
        Update the labels depending on the language.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        pass

    def go_back_to_home(self):
        self.manager.current = "home"
