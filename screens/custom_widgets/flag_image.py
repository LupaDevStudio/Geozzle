"""
Module to create a flag image.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    ColorProperty,
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_IMAGES_FLAG_UNKNOWN
)
from tools.constants import (
    OPACITY_ON_BUTTON_PRESS,
    BUTTON_OUTLINE_WIDTH
)
from tools import sound_mixer

#############
### Class ###
#############


class FlagImage(ButtonBehavior, Image):

    primary_color = ColorProperty((0, 0, 0, 1))
    stretch_mode = StringProperty("height")
    font_ratio = NumericProperty(1)
    outline_width = NumericProperty(BUTTON_OUTLINE_WIDTH)

    def __init__(self,
                 release_function=lambda: 1 + 1,
                 disable_button=False, font_ratio=None, **kw):
        super().__init__(**kw)
        self.source = PATH_IMAGES_FLAG_UNKNOWN
        self.bind(source=self.on_source_change)

        if font_ratio is not None:
            self.font_ratio = font_ratio
        self.release_function = release_function
        self.disable_button = disable_button
        self.always_release = True

    def on_kv_post(self, base_widget):
        if self.stretch_mode == "height":
            self.bind(height=self.on_source_change)
        else:
            self.bind(width=self.on_source_change)
        return super().on_kv_post(base_widget)

    def on_source_change(self, base_widget=None, value=None):
        texture_width, texture_height = self.texture_size
        if self.stretch_mode == "height":
            if texture_height != 0:
                self.width = self.height * texture_width / texture_height
        else:
            if texture_width != 0:
                self.height = self.width * texture_height / texture_width

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS
            sound_mixer.play("click")

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
