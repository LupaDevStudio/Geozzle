"""
Module to create a popup with a custom style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    ColorProperty,
    NumericProperty,
    StringProperty,
    ObjectProperty
)

### Local imports ###

from screens.custom_widgets.custom_popup import CustomPopup
from tools.geozzle import (
    TEXT
)

#############
### Class ###
#############


class ImagePopup(CustomPopup):

    ok_button_label = StringProperty(TEXT.popup["close"])
    release_function = ObjectProperty(lambda: 1 + 1)
    image_source = StringProperty()
    mode = StringProperty("image")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not "release_function" in kwargs:
            self.release_function = self.dismiss

    def close_popup(self):
        self.dismiss()
        self.release_function()
