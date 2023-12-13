"""
Module to create images with text on it and a transparent button.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.image import Image
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    NumericProperty
)

#############
### Class ###
#############


class ImageWithTextButton(Image):
    """
    Image class with a text label on it and a transparent button.
    """

    # Add new attributes to manage the text
    text = StringProperty()
    text_font_name = StringProperty("Roboto")
    text_color = ObjectProperty([0, 1, 0, 1])
    text_filling_ratio = 0.9
    text_halign = "center"
    text_valign = "center"
    text_font_size = NumericProperty(15)
    release_function = ObjectProperty()
