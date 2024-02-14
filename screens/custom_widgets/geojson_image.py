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


class GeojsonImage(Image):

    primary_color = ColorProperty((0, 0, 0, 1))

    def __init__(self, **kw):
        super().__init__(**kw)
        self.source = PATH_IMAGES_FLAG_UNKNOWN
        self.bind(source=self.on_source_change)
        self.bind(height=self.on_source_change)

    def on_source_change(self, base_widget=None, value=None):
        texture_width, texture_height = self.texture_size
        if texture_height != 0:
            self.width = self.height * texture_width / texture_height
