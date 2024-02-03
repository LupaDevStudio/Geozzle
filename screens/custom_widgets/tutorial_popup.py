"""
Module to create a popup with a custom style.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import (
    NumericProperty,
    BooleanProperty,
    StringProperty
)

### Local imports ###

from screens.custom_widgets.custom_popup import CustomPopup

#############
### Class ###
#############


class TutorialPopup(CustomPopup):

    page_id = NumericProperty()
    include_image = BooleanProperty()
    next_button_label = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
