"""
Module to create a popup with a custom style.
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


class TutorialPopup(CustomPopup):

    page_id = NumericProperty()
    include_image = BooleanProperty()
    next_button_label = StringProperty()
    previous_button_label = StringProperty()
    next_button_disabled = BooleanProperty(False)
    previous_button_disabled = BooleanProperty()
    center_label_text = StringProperty()
    side_label_text = StringProperty()
    side_image_source = StringProperty()
    side_image_disabled = BooleanProperty()

    def __init__(self, tutorial_content, **kwargs):
        super().__init__(**kwargs)
        self.next_button_label = TEXT.tutorial["next"]
        self.previous_button_label = TEXT.tutorial["previous"]
        self.close_button_label = TEXT.tutorial["close"]
        self.nb_pages = len(tutorial_content)
        self.tutorial_content = tutorial_content
        self.load_content()

    def load_content(self):
        # Disable the useless buttons
        if self.page_id == 0:
            self.ids["previous_button"].opacity = 0
            self.previous_button_disabled = True
        else:
            self.previous_button_disabled = False
            self.ids["previous_button"].opacity = 1
        if self.page_id == self.nb_pages - 1:
            self.previous_button_disabled = False
            self.next_button_label = TEXT.tutorial["close"]
        else:
            self.close_button_disabled = True
            self.next_button_label = TEXT.tutorial["next"]

        # Switch on the type of content
        current_content = self.tutorial_content[self.page_id]
        if len(current_content) == 2:
            # Text + image
            self.side_label_text = current_content[0]
            self.side_image_source = current_content[1]
            self.side_image_disabled = False
            # Disable useless widgets
            self.center_label_text = ""

        else:
            # Text
            self.center_label_text = current_content[0]
            # Disable useless widgets
            self.side_label_text = ""
            self.side_image_disabled = True

    def go_to_next_page(self, *_):
        self.page_id += 1
        if self.page_id == self.nb_pages:
            self.dismiss()
        else:
            self.load_content()

    def go_to_previous_page(self, *_):
        self.page_id -= 1
        self.load_content()
