"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd
from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from screens.custom_widgets import (
    GeozzleScreen,
    ImagePopup
)
from tools.constants import (
    PRICE_BACKGROUND,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP,
    CUSTOM_BUTTON_BACKGROUND_COLOR,
    CUSTOM_BUTTON_DISABLE_BACKGROUND_COLOR,
    DICT_CONTINENTS,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED
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
    buy_background_label = StringProperty()

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
        self.buy_background_label = TEXT.gallery["buy_background"].replace(
            "[POINTS]", str(PRICE_BACKGROUND))
        if USER_DATA.can_buy_background:
            self.ids.buy_background_button.disable_button = False
            self.ids.buy_background_button.background_color = CUSTOM_BUTTON_BACKGROUND_COLOR
        else:
            self.ids.buy_background_button.disable_button = True
            self.ids.buy_background_button.background_color = CUSTOM_BUTTON_DISABLE_BACKGROUND_COLOR

    def buy_background(self):
        dict_details = USER_DATA.buy_new_background()
        self.reload_language()
        code_continent = dict_details["code_continent"]
        full_path = dict_details["full_path"]
        is_new = dict_details["is_new"]
        if is_new:
            title = TEXT.gallery["new_background"]
        else:
            title = TEXT.gallery["already_bought_background"]

        # Open a popup showing the new bought background
        popup = ImagePopup(
            font_ratio=self.font_ratio,
            primary_color=DICT_CONTINENTS[code_continent],
            secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[code_continent],
            title=title,
            image_source=full_path,
            release_function=partial(self.manager.change_background, background_path=full_path)
        )
        popup.open()
