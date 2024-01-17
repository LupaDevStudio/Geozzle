"""
Module to create the game over screen.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd
import os

### Kivy imports ###

from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    ColorProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_TEXT_FONT,
)
from tools.constants import (
    LIST_CONTINENTS,
    DICT_CONTINENTS,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED,
    TIME_CHANGE_BACKGROUND,
    TEXT
)
from tools.kivy_tools import ImprovedScreen

#############
### Class ###
#############


class GameOverScreen(ImprovedScreen):

    previous_screen_name = StringProperty()
    code_continent = StringProperty(LIST_CONTINENTS[0])
    continent_color = ColorProperty(DICT_CONTINENTS[LIST_CONTINENTS[0]])
    background_color = ColorProperty(
        DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[LIST_CONTINENTS[0]])
    title_label = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + self.code_continent + "/" +
            rd.choice(os.listdir(PATH_BACKGROUNDS + self.code_continent)),
            font_name=PATH_TEXT_FONT,
            **kwargs)

        self.bind(code_continent=self.update_color)
        self.update_text()

    def on_pre_enter(self, *args):

        return super().on_pre_enter(*args)

    def on_enter(self, *args):

        # Schedule the change of background
        Clock.schedule_interval(
            self.manager.change_background, TIME_CHANGE_BACKGROUND)

        return super().on_enter(*args)

    def on_pre_leave(self, *args):

        # Unschedule the clock updates
        Clock.unschedule(self.manager.change_background,
                         TIME_CHANGE_BACKGROUND)

        return super().on_leave(*args)

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
        self.title_label = TEXT.game_over["title"]

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

    def go_back_to_home(self):
        self.manager.get_screen(
            "home").previous_screen_name = "game_over"
        self.manager.current = "home"
