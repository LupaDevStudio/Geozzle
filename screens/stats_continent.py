"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

import os
import random as rd
from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty
)
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_CONTINENTS_IMAGES
)
from screens.custom_widgets import (
    GeozzleScreen,
    CircleProgressBar,
    MyScrollViewLayout,
    StatsLayout
)
from tools.constants import (
    LIST_CONTINENTS,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP,
    SCREEN_ICON_LEFT_DOWN,
    DICT_CONTINENTS,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED,
    HIGHSCORE_FONT_SIZE,
    SUBTITLE_OUTLINE_WIDTH,
    WHITE
)
from tools.geozzle import (
    USER_DATA,
    TEXT,
    SHARED_DATA
)

#############
### Class ###
#############


class StatsContinentScreen(GeozzleScreen):

    code_continent = StringProperty(LIST_CONTINENTS[0])

    dict_type_screen = {
        SCREEN_TITLE: {},
        SCREEN_ICON_LEFT_UP: {},
        SCREEN_ICON_LEFT_DOWN: {}
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=rd.choice(SHARED_DATA.list_unlocked_backgrounds),
            font_name=PATH_TEXT_FONT,
            **kwargs)

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
        self.dict_type_screen[SCREEN_TITLE]["title"] = TEXT.home[self.code_continent]
        self.dict_type_screen[SCREEN_TITLE]["colors"] = DICT_CONTINENTS[self.code_continent]
        self.dict_type_screen[SCREEN_ICON_LEFT_UP]["colors"] = DICT_CONTINENTS[self.code_continent]
        self.dict_type_screen[SCREEN_ICON_LEFT_DOWN]["colors"] = DICT_CONTINENTS[self.code_continent]
        super().reload_language()

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def fill_scrollview(self):
        scrollview_layout: MyScrollViewLayout = self.ids.scrollview_layout

        # TODO

    def on_leave(self, *args):
        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        super().on_leave(*args)
