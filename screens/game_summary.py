"""
Module to create the game screen with the summary of all clues.
"""

###############
### Imports ###
###############

### Python imports ###

import os
import random as rd
from typing import Literal
from functools import partial

### Kivy imports ###

from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    ColorProperty,
    NumericProperty
)
from kivy.uix.label import Label
from screens.custom_widgets.image_popup import ImagePopup

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_TEXT_FONT,
    PATH_IMAGES_FLAG,
    PATH_IMAGES_FLAG_UNKNOWN,
    PATH_IMAGES_GEOJSON
)
from tools.constants import (
    DICT_CONTINENTS_PRIMARY_COLOR,
    LIST_CONTINENTS,
    DICT_CONTINENT_SECOND_COLOR,
    TIME_CHANGE_BACKGROUND,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP,
    SCREEN_THREE_LIVES,
    SCREEN_MULTIPLIER,
    SCREEN_CONTINENT_PROGRESS_BAR
)
from tools.geozzle import (
    USER_DATA,
    TEXT,
    SHARED_DATA

)
from screens.custom_widgets import GeozzleScreen

#############
### Class ###
#############


class ScrollViewLabel(Label):
    pass


class GameSummaryScreen(GeozzleScreen):

    dict_scrollview_widgets = {}
    text_found_country = StringProperty()
    get_new_hint = StringProperty()
    title_label = StringProperty()

    dict_type_screen = {
        SCREEN_TITLE: {},
        SCREEN_ICON_LEFT_UP: {},
        SCREEN_MULTIPLIER: "",
        SCREEN_THREE_LIVES: "",
        SCREEN_CONTINENT_PROGRESS_BAR: ""
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=rd.choice(SHARED_DATA.list_unlocked_backgrounds),
            font_name=PATH_TEXT_FONT,
            **kwargs)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        self.update_scroll_view()
        self.update_images()

        if len(USER_DATA.game.list_current_clues) < 2:
            self.ids.scrollview.scroll_y = 1

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

        self.text_found_country = TEXT.game_summary["i_found"]
        self.get_new_hint = TEXT.game_summary["new_hint"]
        self.title_label = TEXT.game_summary["title"]

        super().reload_language()

    def update_images(self):
        # Update the flag image
        if "flag" in USER_DATA.game.dict_guessed_countries[USER_DATA.game.current_guess_country]["list_clues"]:
            self.ids.flag_image.reload()
            self.ids.flag_image.source = PATH_IMAGES_FLAG + USER_DATA.game.current_guess_country + ".png"
            self.ids.flag_image.disable_button = False
        else:
            self.ids.flag_image.source = PATH_IMAGES_FLAG_UNKNOWN
            self.ids.flag_image.disable_button = True

        # Update the geojson image
        if "ISO_3_code" in USER_DATA.game.dict_guessed_countries[USER_DATA.game.current_guess_country]["list_clues"]:
            self.ids.geojson_image.reload()
            self.ids.geojson_image.source = PATH_IMAGES_GEOJSON + USER_DATA.game.dict_details_country[TEXT.language]["ISO_3_code"] + \
                ".png"
            self.ids.geojson_image.disable_button = False
        else:
            self.ids.geojson_image.source = PATH_IMAGES_FLAG_UNKNOWN
            self.ids.geojson_image.disable_button = True

    def reset_scroll_view(self, *_):
        """
        Remove all the labels in the scrollview.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.ids.scrollview_layout.reset_scrollview()
        self.dict_scrollview_widgets = {}

    def update_scroll_view(self):
        """
        Add the labels of clues in the scrollview.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for code_clue in USER_DATA.game.dict_guessed_countries[USER_DATA.game.current_guess_country]["list_clues"]:
            if not code_clue in ["flag", "ISO_3_code"]:

                # Add the labels which are not already in the scrollview
                if not code_clue in self.dict_scrollview_widgets:

                    label_clue = ScrollViewLabel(
                        text=USER_DATA.game.dict_details_country[TEXT.language][code_clue],
                        color=self.continent_color,
                        font_name=self.font_name,
                        font_size=17 * self.font_ratio,
                        halign="left",
                        valign="middle",
                        shorten=False,
                        line_height=1
                    )
                    self.ids.scrollview_layout.add_widget(label_clue)

                    self.dict_scrollview_widgets[code_clue] = label_clue

    def go_to_game_over(self):
        self.manager.get_screen(
            "game_over").previous_screen_name = "game_summary"
        self.manager.current = "game_over"

    def go_to_game_question(self):
        self.manager.get_screen(
            "game_question").previous_screen_name = "game_summary"
        self.manager.current = "game_question"

    def open_popup_image(self, mode: Literal["flag", "geojson"]):
        if mode == "flag":
            image_source = PATH_IMAGES_FLAG + USER_DATA.game.current_guess_country + ".png"
        elif mode == "geojson":
            image_source = PATH_IMAGES_GEOJSON + \
                USER_DATA.game.dict_details_country[TEXT.language]["ISO_3_code"] + ".png"
        popup = ImagePopup(
            primary_color=self.continent_color,
            secondary_color=self.secondary_continent_color,
            title=TEXT.game_summary["zoom_" + mode + "_title"],
            font_ratio=self.font_ratio,
            image_source=image_source,
            ok_button_label=TEXT.home["cancel"]
        )
        popup.mode = mode
        popup.open()

    def open_popup_flag(self):
        self.open_popup_image("flag")

    def open_popup_geojson(self):
        self.open_popup_image("geojson")
