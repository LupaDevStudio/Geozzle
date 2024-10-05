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
    ColorProperty,
    ObjectProperty,
    BooleanProperty
)

### Local imports ###

from tools.path import (
    PATH_IMAGES
)
from tools.constants import (
    WHITE,
    BLACK
)

#############
### Class ###
#############


class ThreeLives(RelativeLayout):
    """
    The indicator of lives.
    """

    continent_color = ColorProperty(BLACK)
    background_color = ColorProperty(WHITE)
    number_lives_on = NumericProperty(3)
    image_path_1 = StringProperty(PATH_IMAGES + "life_on.png")
    image_path_2 = StringProperty(PATH_IMAGES + "life_on.png")
    image_path_3 = StringProperty(PATH_IMAGES + "life_on.png")
    release_function = ObjectProperty(lambda: 1 + 1)
    disable_button = BooleanProperty(False)
    font_ratio = NumericProperty(1)

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
