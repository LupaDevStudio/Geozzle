"""
Module to create a popup to allow the user to regenerate lives.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty
)

### Local imports ###

from screens.custom_widgets.custom_popup import CustomPopup
from tools.geozzle import (
    TEXT
)

#############
### Class ###
#############


class EndCountryPopup(CustomPopup):
    
    popup_size = ObjectProperty((0.85, 0.45))
    ok_button_label = StringProperty(TEXT.popup["close"])
    score_text = StringProperty()
    release_function = ObjectProperty(lambda: 1 + 1)

    country_name = StringProperty()
    multiplier_image = StringProperty()
    new_image = StringProperty()
    nb_stars = NumericProperty()
    flag_image = StringProperty()

    def confirm(self):
        self.dismiss()
        self.release_function()
