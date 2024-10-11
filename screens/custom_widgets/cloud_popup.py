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
    BooleanProperty
)

### Local imports ###

from screens.custom_widgets.custom_popup import CustomPopup
from tools.geozzle import (
    TEXT
)

#############
### Class ###
#############


class CloudPopup(CustomPopup):

    popup_size = ObjectProperty((0.85, 0.75))
    title = StringProperty()
    right_button_label = StringProperty()
    right_release_function = ObjectProperty(lambda: 1 + 1)
    left_button_label = StringProperty(TEXT.popup["cancel"])
    left_release_function = ObjectProperty(lambda: 1 + 1)
    close_button_label = StringProperty()
    close_release_function = ObjectProperty(lambda: 1 + 1)
    center_label_text = StringProperty()
    auto_dismiss_right = BooleanProperty(True)
    unique_id = StringProperty()

    def left_function(self):
        self.dismiss()
        self.left_release_function()

    def close_function(self):
        self.dismiss()
        self.close_release_function()

    def right_function(self):
        if self.auto_dismiss_right:
            self.dismiss()
        self.right_release_function()

class ImportPopup(CustomPopup):

    title = StringProperty()
    right_button_label = StringProperty()
    right_release_function = ObjectProperty(lambda: 1 + 1)
    left_button_label = StringProperty(TEXT.popup["cancel"])
    left_release_function = ObjectProperty(lambda: 1 + 1)
    center_label_text = StringProperty()
    warning_label_text = StringProperty()
    auto_dismiss_right = BooleanProperty(True)
    id_hint_text = StringProperty()

    def left_function(self):
        self.dismiss()
        self.left_release_function()

    def right_function(self):
        if self.auto_dismiss_right:
            self.dismiss()
        text_text_input = self.ids.id_text_input.get_input_text()
        self.right_release_function(user_id=text_text_input)
