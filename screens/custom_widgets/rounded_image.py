"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ObjectProperty,
)

### Local imports ###

from tools.constants import (
    CUSTOM_BUTTON_BACKGROUND_COLOR,
)

#############
### Class ###
#############


class RoundedImage(RelativeLayout):
    """
    A custom button with a white round rectangle background.
    """

    background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
    image_path = StringProperty()
    colors = ObjectProperty()
    radius = NumericProperty(20)

    def __init__(
            self,
            image_path: str = "",
            colors=(0, 0, 0, 1),
            **kwargs):
        super().__init__(**kwargs)

        self.image_path = image_path
        self.colors = colors
