"""
Module to create a flag image.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.image import Image
from kivy.properties import ColorProperty

### Local imports ###

from tools.path import (
    PATH_IMAGES_FLAG_UNKNOWN
)

#############
### Class ###
#############

class FlagImage(Image):

    primary_color = ColorProperty((0, 0, 0, 1))

    def __init__(self, **kw):
        super().__init__(**kw)
        self.source = PATH_IMAGES_FLAG_UNKNOWN
