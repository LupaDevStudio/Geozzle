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
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_IMAGES
)

#############
### Class ###
#############


class ThreeLives(RelativeLayout):
    """
    The indicator of lives.
    """

    continent_color = ColorProperty((0,0,0,1))
    number_lives_on = NumericProperty(3)
    image_path_1 = StringProperty(PATH_IMAGES + "life_on.png")
    image_path_2 = StringProperty(PATH_IMAGES + "life_on.png")
    image_path_3 = StringProperty(PATH_IMAGES + "life_on.png")

    def __init__(
            self,
            **kwargs):
        super().__init__(**kwargs)

        self.bind(number_lives_on=self.update_lives)
        self.bind(continent_color=self.bind_function)

    def bind_function(self, base_widget, value):
        pass

    def update_lives(self, base_widget, value):
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
