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


class TwoButtonsPopup(CustomPopup):

    title = StringProperty()
    left_button_label = StringProperty()
    left_release_function = ObjectProperty()
    right_button_label = StringProperty(TEXT.home["cancel"])
    right_release_function = ObjectProperty()
    center_label_text = StringProperty()

    def __init__(self, **kwargs):
        if not "right_release_function" in kwargs:
            super().__init__(right_release_function=self.dismiss, **kwargs)
        else:
            super().__init__(**kwargs)

        self.bind(left_button_label=self.bind_function)
        self.bind(left_release_function=self.bind_function)
        self.bind(right_button_label=self.bind_function)
        self.bind(right_release_function=self.bind_function)
        self.bind(center_label_text=self.bind_function)
        self.bind(title=self.bind_function)

    def bind_function(self, *args):
        pass
