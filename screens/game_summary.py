"""
Module to create the game screen with the summary of all clues.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    ObjectProperty,
    StringProperty,
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS
)
from tools.constants import (
    DICT_CONTINENTS,
    LIST_CONTINENTS,
    TEXT
)
from tools.kivy_tools import ImprovedScreen

#############
### Class ###
#############


class GameSummaryScreen(ImprovedScreen):
        
    code_continent = StringProperty(LIST_CONTINENTS[0])
    continent_color = ColorProperty(DICT_CONTINENTS[LIST_CONTINENTS[0]])
    # continent_color = ObjectProperty((1,0,0,1)) # TODO

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "lake_sunset.jpg",
            **kwargs)
        
    def update_color(self, base_widget, value):
        """
        Update the code of the continent and its related attributes.

        Parameters
        ----------
        base_widget : kivy.uix.widget
            Self
        value : string
            Value of code_continent

        Returns
        -------
        None
        """
        self.continent_color = DICT_CONTINENTS[self.code_continent]

    def go_back_to_home(self):
        self.manager.current = "home"
