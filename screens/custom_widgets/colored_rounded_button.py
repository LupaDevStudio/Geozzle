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
    OPACITY_ON_BUTTON_PRESS
)

#############
### Class ###
#############


class ColoredRoundedButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a colored round rectangle background.
    """

    background_color = ColorProperty()
    image_path = StringProperty()
    colors = ObjectProperty()
    radius = NumericProperty(20)
    disable_button = BooleanProperty()

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
        self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        self.opacity = 1
