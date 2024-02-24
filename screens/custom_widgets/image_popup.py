"""
Module to create a popup with a custom style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from email.mime import image
from kivy.properties import (
    ColorProperty,
    NumericProperty,
    StringProperty,
    ObjectProperty
)

### Local imports ###

from screens.custom_widgets.custom_popup import CustomPopup
from tools.constants import (
    TEXT
)

#############
### Class ###
#############


class ImagePopup(CustomPopup):

    ok_button_label = StringProperty(TEXT.home["cancel"])
    release_function = ObjectProperty()
    image_source = StringProperty()
    mode = StringProperty()

    def __init__(self, **kwargs):
        if not "release_function" in kwargs:
            super().__init__(release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)
