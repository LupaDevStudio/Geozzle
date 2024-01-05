"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ObjectProperty,
    BooleanProperty
)

### Local imports ###

from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    OPACITY_ON_BUTTON_PRESS
)

#############
### Class ###
#############


class RoundedButtonImage(ButtonBehavior, RelativeLayout):
    """
    A custom button with a white round rectangle background.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    image_path = StringProperty()
    colors = ObjectProperty()
    radius = NumericProperty(20)

    def __init__(
            self,
            image_path:str="",
            colors=(0, 0, 0, 1),
            **kwargs):
        super().__init__(**kwargs)

        self.image_path = image_path
        self.colors = colors
        self.always_release = True

    def on_press(self):
        if not self.disabled:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disabled:
            self.opacity = 1
