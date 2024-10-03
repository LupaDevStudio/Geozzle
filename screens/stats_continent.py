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
    PATH_FLAG_IMAGES,
    PATH_CONTINENTS_IMAGES
)
from screens.custom_widgets import (
    GeozzleScreen,
    MyScrollViewLayout,
    CountryStatCard
)
from tools.constants import (
    LIST_CONTINENTS,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP,
    SCREEN_ICON_LEFT_DOWN,
    DICT_CONTINENTS_PRIMARY_COLOR,
    DICT_CONTINENT_SECOND_COLOR,
    HIGHSCORE_FONT_SIZE,
    SUBTITLE_OUTLINE_WIDTH,
    WHITE,
    DICT_COUNTRIES
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
        super().reload_language()

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def fill_scrollview(self):
        scrollview_layout: MyScrollViewLayout = self.ids.scrollview_layout

        for country_code in DICT_COUNTRIES[USER_DATA.language][self.code_continent]:
            country_name = DICT_COUNTRIES[USER_DATA.language][self.code_continent][country_code]
            flag_image = PATH_FLAG_IMAGES + country_code + ".png"
            number_stars = 0
            if country_code in USER_DATA.stats[self.code_continent]:
                number_stars = USER_DATA.stats[self.code_continent][country_code]["nb_stars"]
            width_card = (Window.size[0]*0.9 - 10*4*self.font_ratio)/3
            height_card = 100*self.font_ratio

            country_card = CountryStatCard(
                font_ratio=self.font_ratio,
                size_hint=(None, None),
                height=height_card,
                width=width_card,
                flag_image=flag_image,
                number_stars=number_stars,
                country_name=country_name,
                color=DICT_CONTINENTS_PRIMARY_COLOR[self.code_continent]
            )
            scrollview_layout.add_widget(country_card)

    def on_leave(self, *args):
        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        super().on_leave(*args)
