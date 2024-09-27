"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from screens.custom_widgets import GeozzleScreen
from tools.constants import (
    BLACK,
    GRAY,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP
)
from tools.geozzle import (
    USER_DATA,
    TEXT,
    SHARED_DATA
)

#############
### Class ###
#############


class GalleryScreen(GeozzleScreen):

    points_label = StringProperty()

    dict_type_screen = {
        SCREEN_TITLE: "gallery",
        SCREEN_ICON_LEFT_UP: {}
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=rd.choice(SHARED_DATA.list_unlocked_backgrounds),
            font_name=PATH_TEXT_FONT,
            **kwargs)

        self.reload_language()

    def reload_language(self):
        """
        Update the labels depending on the language.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        super().reload_language()
        self.points_label = TEXT.gallery["points"].replace(
            "[POINTS]", str(USER_DATA.points))
