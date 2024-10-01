"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ColorProperty,
    ObjectProperty,
    ListProperty
)

### Local imports ###
from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    BUTTON_FONT_SIZE,
    SMALL_BUTTON_FONT_SIZE,
    BLACK,
    WHITE,
    DICT_CONTINENTS
)

SHORT_CONTINENT_NAMES = {
    "Europe": "EUR",
    "Asia": "ASI",
    "Africa": "AFR",
    "North_America": "NAM",
    "South_America": "SAM",
    "Oceania": "OCE"
}

#############
### Class ###
#############


class ContinentProgressBar(RelativeLayout):
    """
    Progress bar showing the completed, actual and remaining continents.
    """

    background_color = ColorProperty(WHITE)
    color = ColorProperty(BLACK)

    text_font_name = StringProperty(PATH_TEXT_FONT)
    text_filling_ratio = NumericProperty(0.8)
    font_size = NumericProperty(SMALL_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)

    continents_list = ListProperty([""] * 6)
    short_continents_list = ListProperty([""] * 6)
    cursor_position = NumericProperty()
    continent_colors = ListProperty([WHITE] * 6)

    def __init__(self, **kw):
        super().__init__(**kw)
        print(self.continents_list)

        self.bind(continents_list=self.disp_continents)

    def disp_continents(self, *_):
        self.continent_colors = [DICT_CONTINENTS[continent]
                                 for continent in self.continents_list]
        self.short_continents_list = [
            SHORT_CONTINENT_NAMES[continent] for continent in self.continents_list]
