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


class TwoButtonsPopup(CustomPopup):

    title = StringProperty()
    right_button_label = StringProperty()
    right_release_function = ObjectProperty(lambda: 1 + 1)
    left_button_label = StringProperty(TEXT.popup["cancel"])
    left_release_function = ObjectProperty(lambda: 1 + 1)
    center_label_text = StringProperty()

    def left_function(self):
        self.dismiss()
        self.left_release_function()

    def right_function(self):
        self.dismiss()
        self.right_release_function()