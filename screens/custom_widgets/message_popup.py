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
from tools.constants import (
    TEXT
)

#############
### Class ###
#############


class MessagePopup(CustomPopup):

    ok_button_label = StringProperty(TEXT.home["cancel"])
    center_label_text = StringProperty()
    release_function = ObjectProperty()

    def __init__(self, **kwargs):
        if not "release_function" in kwargs:
            super().__init__(release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)
