"""
Module to create images with text on it.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.image import Image
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ColorProperty,
    NumericProperty
)

#############
### Class ###
#############


class ImageWithText(Image):
    """
    Image class with a text label on it.
    """

    # Add new attributes to manage the text
    text = StringProperty()
    text_font_name = StringProperty("Roboto")
    text_color = ObjectProperty([0, 1, 0, 1])
    text_filling_ratio = 0.9
    text_halign = "center"
    text_valign = "center"
    text_font_size = 15
    text_outline_color = ColorProperty()
    text_outline_width = NumericProperty()
