"""
Module to create a popup to allow the user to regenerate lives.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.properties import (
    ObjectProperty,
    StringProperty
)

### Local imports ###

from screens.custom_widgets.custom_popup import CustomPopup
from tools import (
    game
)
from tools.constants import (
    TEXT
)

#############
### Class ###
#############


class TwoButtonsImagePopup(CustomPopup):

    title = StringProperty()
    right_button_label = StringProperty()
    right_release_function = ObjectProperty()
    left_button_label = StringProperty(TEXT.home["cancel"])
    left_release_function = ObjectProperty()
    center_label_text = StringProperty()
    image_source = StringProperty()

    def __init__(self, **kwargs):
        if not "left_release_function" in kwargs:
            super().__init__(left_release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)
