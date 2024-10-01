"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ColorProperty,
    ObjectProperty
)

### Local imports ###
from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    BUTTON_FONT_SIZE,
    SMALL_BUTTON_FONT_SIZE,
    BLACK,
    WHITE
)
from tools import sound_mixer

#############
### Class ###
#############


class StatsLayout(RelativeLayout):
    """
    The stats layout.
    """

    background_color = ColorProperty(WHITE)
    color_label = ColorProperty(BLACK)
    background_button_color = ColorProperty(WHITE)

    text = StringProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    text_filling_ratio = NumericProperty(0.8)
    font_size = NumericProperty(BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)

    text_button = StringProperty()
    release_function = ObjectProperty(lambda: 1 + 1)

class CountryStatCard(RelativeLayout):
    """
    The stat layout for a country.
    """

    background_color = ColorProperty(WHITE)
    color = ColorProperty(BLACK)

    country_name = StringProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    text_filling_ratio = NumericProperty(0.8)
    font_size = NumericProperty(SMALL_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)

    number_stars = NumericProperty(0)
    flag_image = StringProperty()
