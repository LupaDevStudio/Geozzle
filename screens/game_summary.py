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
    DICT_CONTINENTS,
    LIST_CONTINENTS,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED,
    TIME_CHANGE_BACKGROUND,
    TEXT
)
from screens.custom_widgets import ImprovedScreenWithAds
from tools import (
    game
)

#############
### Class ###
#############


class ScrollViewLabel(Label):
    pass


class GameSummaryScreen(ImprovedScreenWithAds):

    previous_screen_name = StringProperty()
    code_continent = StringProperty(LIST_CONTINENTS[0])
    continent_color = ColorProperty(DICT_CONTINENTS[LIST_CONTINENTS[0]])
    background_color = ColorProperty(
        DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[LIST_CONTINENTS[0]])
    number_lives_on = NumericProperty()
    dict_scrollview_widgets = {}
    text_found_country = StringProperty()
    current_hint = StringProperty()  # the name of the new hint
    get_new_hint = StringProperty()
    title_label = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + self.code_continent + "/" +
            rd.choice(os.listdir(PATH_BACKGROUNDS + self.code_continent)),
            font_name=PATH_TEXT_FONT,
            **kwargs)

        self.bind(code_continent=self.update_color)
        self.bind(current_hint=self.bind_function)
        self.update_text()

    def on_pre_enter(self, *args):
        self.update_font_ratio()
        self.update_scroll_view()
        self.update_text()
        self.update_images()

        return super().on_pre_enter(*args)

    def on_enter(self, *args):

        if len(game.dict_clues[TEXT.language]) < 2:
            self.ids.scrollview.scroll_y = 1

        # Schedule the change of background
        Clock.schedule_interval(
            self.manager.change_background, TIME_CHANGE_BACKGROUND)

        self.number_lives_on = game.number_lives

        return super().on_enter(*args)

    def on_pre_leave(self, *args):

        # Unschedule the clock updates
        Clock.unschedule(self.manager.change_background,
                         TIME_CHANGE_BACKGROUND)

        return super().on_leave(*args)

    def bind_function(self, base_widget, value):
        pass

    def update_text(self):
        """
        Update the labels depending on the language.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.text_found_country = TEXT.game_summary["i_found"]
        self.get_new_hint = TEXT.game_summary["new_hint"]
        self.title_label = TEXT.game_summary["title"]

    def update_images(self):
        # Update the flag image
        if "flag" in game.dict_clues[TEXT.language]:
            self.ids.flag_image.reload()
            self.ids.flag_image.source = PATH_IMAGES_FLAG + self.code_continent.lower() + \
                ".png"
            self.ids.flag_image.disable_button = False
        else:
            self.ids.flag_image.source = PATH_IMAGES_FLAG_UNKNOWN
            self.ids.flag_image.disable_button = True

        # Update the geojson image
        if "ISO_3_code" in game.dict_clues[TEXT.language]:
            self.ids.geojson_image.reload()
            self.ids.geojson_image.source = PATH_IMAGES_GEOJSON + game.dict_clues[TEXT.language]["ISO_3_code"] + \
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
        self.ids.scrollview_layout.reset_screen()
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
        for key in game.dict_clues[TEXT.language]:
            if not key in ["flag", "ISO_3_code"]:

                # Add the labels which are not already in the scrollview
                if not key in self.dict_scrollview_widgets:

                    label_clue = ScrollViewLabel(
                        text=game.dict_clues[TEXT.language][key],
                        color=self.continent_color,
                        font_name=self.font_name,
                        font_size=17 * self.font_ratio,
                        halign="left",
                        valign="middle",
                        shorten=False,
                        line_height=1
                    )
                    self.ids.scrollview_layout.add_widget(label_clue)

                    self.dict_scrollview_widgets[key] = label_clue

            else:
                self.update_images()

    def update_color(self, base_widget, value):
        """
        Update the code of the continent and its related attributes.

        Parameters
        ----------
        base_widget : kivy.uix.widget
            Self
        value : string
            Value of code_continent

        Returns
        -------
        None
        """
        self.continent_color = DICT_CONTINENTS[self.code_continent]
        self.background_color = DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[
            self.code_continent]

    def go_to_game_over(self):
        self.manager.get_screen(
            "game_over").previous_screen_name = "game_summary"
        self.manager.current = "game_over"

    def go_to_game_question(self):
        self.manager.get_screen(
            "game_question").previous_screen_name = "game_summary"
        self.manager.current = "game_question"

    def go_back_to_home(self):
        self.manager.get_screen(
            "home").previous_screen_name = "game_summary"
        self.manager.current = "home"

    def open_popup_image(self, mode: Literal["flag", "geojson"]):
        if mode == "flag":
            image_source = PATH_IMAGES_FLAG + self.code_continent.lower() + ".png"
        elif mode == "geojson":
            image_source = PATH_IMAGES_GEOJSON + \
                game.dict_clues[TEXT.language]["ISO_3_code"] + ".png"
            print(image_source)
        popup = ImagePopup(
            primary_color=self.continent_color,
            secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[self.code_continent],
            title=TEXT.game_summary["zoom_" + mode + "_title"],
            font_ratio=self.font_ratio,
            image_source=image_source
        )
        popup.mode = mode
        popup.open()

    def open_popup_flag(self):
        self.open_popup_image("flag")

    def open_popup_geojson(self):
        self.open_popup_image("geojson")
