"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

### Local imports ###

from tools.constants import (
    OPACITY_ON_BUTTON_PRESS
)
from tools import sound_mixer

#############
### Class ###
#############


class CircleIconButton(ButtonBehavior, Image):
    """
    A custom button with a white round rectangle background.
    """

    def __init__(
            self,
            release_function=lambda: 1 + 1, **kwargs):
        super().__init__(**kwargs)
        self.release_function = release_function
        self.always_release = True

    def on_press(self):
        self.opacity = OPACITY_ON_BUTTON_PRESS
        sound_mixer.play("click")

    def on_release(self):
        self.release_function()
        self.opacity = 1
