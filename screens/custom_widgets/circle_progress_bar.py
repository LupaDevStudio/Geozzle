"""
Module to create custom buttons with round transparent white background.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.image import Image
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ColorProperty
)

### Local imports ###

from tools.constants import (
    OPACITY_ON_BUTTON_PRESS
)

#############
### Class ###
#############


class CircleProgressBar(Image):
    """
    A custom progress bar with a circle and 
    """

    progress = NumericProperty()
    progress_angle = NumericProperty()
    circle_color = ColorProperty()
    font_ratio = NumericProperty(1)
    completion_label_text = StringProperty()

    def __init__(
            self,
            **kwargs):
        super().__init__(**kwargs)
        self.bind(progress=self.update_progress_angle)

    def update_progress_angle(self, value, base_widget):
        self.progress_angle = self.progress / 100 * 360
        self.completion_label_text = f"{int(self.progress)}%"
