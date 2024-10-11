"""
Module to create a custom text input with an icon on the left.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.relativelayout import RelativeLayout
from kivy.core.clipboard import Clipboard
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ColorProperty,
    NumericProperty
)

### Local imports ###

from tools.constants import (
    BLACK,
    GRAY,
    SMALL_SCORE_FONT_SIZE
)
from tools.path import (
    PATH_TEXT_FONT
)

#############
### Class ###
#############


class CustomTextInput(RelativeLayout):
    """
    A custom text input with an icon on the left.
    """

    hint_text = StringProperty()
    write_mode = BooleanProperty(True)
    copy_mode = BooleanProperty(False)

    primary_color = ColorProperty(BLACK)
    secondary_color = ColorProperty(GRAY)

    font_ratio = NumericProperty(1)
    font_size = NumericProperty(SMALL_SCORE_FONT_SIZE)
    path_font = StringProperty(PATH_TEXT_FONT)

    line_width = NumericProperty(1)

    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_input_text(self):
        return self.ids.text_input.text

    def copy_text(self):
        Clipboard.copy(self.get_input_text())
