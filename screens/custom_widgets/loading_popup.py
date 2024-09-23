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

from tools.geozzle import (
    TEXT
)

#############
### Class ###
#############


class LoadingPopup(CustomPopup):

    title = StringProperty()
    center_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.center_text = TEXT.popup["loading"]
        self.title = TEXT.popup["loading_title"]
