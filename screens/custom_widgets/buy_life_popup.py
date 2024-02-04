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
    TEXT,
)

#############
### Class ###
#############


class BuyLifePopup(CustomPopup):

    buy_button_label = StringProperty(TEXT.home["watch_ad"])
    cancel_button_label = StringProperty(TEXT.home["cancel"])
    center_label_text = StringProperty(TEXT.home["buy_life_message"])
    title = StringProperty(TEXT.home["buy_life_title"])
    release_function = ObjectProperty()

    def __init__(self, **kwargs):
        if not "release_function" in kwargs:
            super().__init__(release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)

        self.bind(cancel_button_label=self.bind_function)
        self.bind(release_function=self.bind_function)
        self.bind(title=self.bind_function)

    def bind_function(self, *args):
        pass

    def watch_ad(self):
        print("WATCH AD")
        pass
