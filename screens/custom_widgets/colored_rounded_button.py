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
    ColorProperty,
    ObjectProperty
)

### Local imports ###
from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    MAIN_BUTTON_FONT_SIZE,
    OPACITY_ON_BUTTON_PRESS,
    BLACK,
    TRANSPARENT
)
from tools import sound_mixer

#############
### Class ###
#############


class ColoredRoundedButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a colored round rectangle background.
    """

    background_color = ColorProperty()
    text = StringProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    text_filling_ratio = NumericProperty(0.8)
    font_size = NumericProperty(MAIN_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    disable_button = BooleanProperty(False)
    color_label = ColorProperty(BLACK)
    release_function = ObjectProperty(lambda: 1 + 1)

    shadow_color = ColorProperty(BLACK)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.shadow_color = TRANSPARENT
            self.opacity = OPACITY_ON_BUTTON_PRESS
            sound_mixer.play("click")

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
            self.shadow_color = BLACK

class ColoredRoundedHintButton(ButtonBehavior, RelativeLayout):
    """
    A custom button with a colored round rectangle background and the number of stars for each hint.
    """

    background_color = ColorProperty()
    text = StringProperty()
    text_font_name = StringProperty(PATH_TEXT_FONT)
    text_filling_ratio = NumericProperty(0.9)
    font_size = NumericProperty(MAIN_BUTTON_FONT_SIZE)
    font_ratio = NumericProperty(1)
    disable_button = BooleanProperty(False)
    color_label = ColorProperty(BLACK)
    release_function = ObjectProperty(lambda: 1 + 1)
    number_stars = NumericProperty(1)

    shadow_color = ColorProperty(BLACK)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.shadow_color = TRANSPARENT
            self.opacity = OPACITY_ON_BUTTON_PRESS
            sound_mixer.play("click")

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
            self.shadow_color = BLACK
