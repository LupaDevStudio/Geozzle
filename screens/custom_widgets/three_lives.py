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
    ColorProperty,
    ObjectProperty,
    BooleanProperty
)

### Local imports ###

from tools.path import (
    PATH_IMAGES
)
from tools.constants import (
    OPACITY_ON_BUTTON_PRESS
)
from tools import (
    sound_mixer
)

#############
### Class ###
#############


class ThreeLives(ButtonBehavior, RelativeLayout):
    """
    The indicator of lives.
    """

    continent_color = ColorProperty((0, 0, 0, 1))
    number_lives_on = NumericProperty(3)
    image_path_1 = StringProperty(PATH_IMAGES + "life_on.png")
    image_path_2 = StringProperty(PATH_IMAGES + "life_on.png")
    image_path_3 = StringProperty(PATH_IMAGES + "life_on.png")
    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)

    def __init__(self, ** kwargs):
        super().__init__(**kwargs)

        self.always_release = True

        self.bind(number_lives_on=self.update_lives)
        self.update_lives()

    def update_lives(self, *args):
        if self.number_lives_on >= 1:
            self.image_path_3 = PATH_IMAGES + "life_on.png"
        else:
            self.image_path_3 = PATH_IMAGES + "life_off.png"

        if self.number_lives_on >= 2:
            self.image_path_2 = PATH_IMAGES + "life_on.png"
        else:
            self.image_path_2 = PATH_IMAGES + "life_off.png"

        if self.number_lives_on >= 3:
            self.image_path_1 = PATH_IMAGES + "life_on.png"
        else:
            self.image_path_1 = PATH_IMAGES + "life_off.png"

    def on_press(self):
        if not self.disable_button:
            self.opacity = OPACITY_ON_BUTTON_PRESS
            sound_mixer.play("click")

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
