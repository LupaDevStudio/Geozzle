"""
Module to create a popup to allow the user to regenerate lives.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.properties import (
    NumericProperty,
    BooleanProperty,
    StringProperty
)

### Local imports ###

from screens.custom_widgets.custom_popup import CustomPopup
from tools.constants import (
    TEXT,
)

#############
### Class ###
#############


class BuyLifePopup(CustomPopup):

    buy_button_label = StringProperty()
    cancel_button_label = StringProperty()
    center_label_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.buy_button_label = TEXT.home["watch_ad"]
        self.cancel_button_label = TEXT.home["cancel"]
        self.center_label_text = TEXT.home["buy_life_message"]
        self.title = "Vies épuisées"

    def watch_ad(self):
        pass
