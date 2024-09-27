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
    ObjectProperty,
    BooleanProperty,
    ColorProperty
)

### Local imports ###

from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    OPACITY_ON_BUTTON_PRESS,
    BLACK
)
from tools import sound_mixer

#############
### Class ###
#############


class RoundedButtonImage(ButtonBehavior, RelativeLayout):
    """
    A custom button with a white round rectangle background.
    """

    disable_button = BooleanProperty(False)
    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    image_path = StringProperty()
    colors = ColorProperty(BLACK)
    radius = NumericProperty(20)
    release_function = ObjectProperty(lambda: 1 + 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS
            sound_mixer.play("click")

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
