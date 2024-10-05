"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.uix.slider import Slider
from kivy.properties import (
    NumericProperty,
    ColorProperty
)

### Local imports ###

from tools.constants import (
    BLACK,
    WHITE
)


#############
### Class ###
#############


class CustomSlider(Slider):
    """
    A custom slider.
    """

    primary_color = ColorProperty(BLACK)
    secondary_color = ColorProperty(WHITE)

    font_ratio = NumericProperty(1)

    def __init__(
            self,
            **kwargs):
        super().__init__(**kwargs)
        self.cursor_width = 0
        self.cursor_height = 0
        self.border_horizontal = [0, 0, 0, 0]
