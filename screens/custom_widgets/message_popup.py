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


class MessagePopup(CustomPopup):

    popup_size = ObjectProperty((0.85, 0.4))
    ok_button_label = StringProperty(TEXT.popup["close"])
    center_label_text = StringProperty()
    release_function = ObjectProperty(lambda: 1 + 1)

    def confirm(self):
        self.dismiss()
        self.release_function()
