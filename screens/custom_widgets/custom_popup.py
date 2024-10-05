"""
Module to create a popup with a custom style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.popup import Popup
from kivy.properties import (
    ColorProperty,
    NumericProperty,
    ObjectProperty
)

### Local imports ###

from tools.constants import (
    BLACK,
    WHITE
)

#############
### Class ###
#############


class CustomPopup(Popup):

    popup_size = ObjectProperty((0.85,0.6))
    title_color = ColorProperty(BLACK)
    primary_color = ColorProperty(BLACK)
    secondary_color = ColorProperty(WHITE)
    font_ratio = NumericProperty(1)
