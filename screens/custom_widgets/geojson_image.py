"""
Module to create a flag image.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import ColorProperty

### Local imports ###

from tools.path import (
    PATH_IMAGES_FLAG_UNKNOWN
)
from tools.constants import (
    OPACITY_ON_BUTTON_PRESS
)
from tools import sound_mixer

#############
### Class ###
#############


class GeojsonImage(ButtonBehavior, Image):

    primary_color = ColorProperty((0, 0, 0, 1))

    def __init__(self,
            release_function=lambda: 1 + 1,
            disable_button=False, **kw):
        super().__init__(**kw)
        self.source = PATH_IMAGES_FLAG_UNKNOWN
        self.bind(source=self.on_source_change)
        self.bind(height=self.on_source_change)
        self.release_function = release_function
        self.disable_button = disable_button
        self.always_release = True

    def on_source_change(self, base_widget=None, value=None):
        texture_width, texture_height = self.texture_size
        if texture_height != 0:
            self.width = self.height * texture_width / texture_height

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS
            sound_mixer.play("click")

    def on_release(self):
        if not self.disable_button:
            self.release_function()
            self.opacity = 1
