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
    BooleanProperty,
    ColorProperty
)

### Local imports ###
from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    MAIN_BUTTON_FONT_SIZE,
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
    text = StringProperty()
    text_filling_ratio = NumericProperty()
    font_size = NumericProperty()
    font_ratio = NumericProperty(1)
    disable_button = BooleanProperty(False)
    color_label = ColorProperty()

    def __init__(
            self,
            text="",
            text_font_name=PATH_TEXT_FONT,
            text_filling_ratio=0.8,
            font_size=MAIN_BUTTON_FONT_SIZE,
            release_function=lambda: 1 + 1,
            font_ratio=None,
            **kwargs):
        if font_ratio is not None:
            self.font_ratio = font_ratio
        super().__init__(**kwargs)
        self.release_function = release_function
        self.always_release = True
        self.text_font_name = text_font_name
        self.text = text
        self.text_filling_ratio = text_filling_ratio
        self.font_size = font_size

        self.bind(disable_button=self.my_function)
        self.bind(color_label=self.my_function)
        self.bind(background_color=self.my_function)

    def my_function(self, base_widget, value):
        pass

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS

    def on_release(self):
        if not self.disable_button:
            self.release_function()
            self.opacity = 1
