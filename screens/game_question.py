"""
Module to create the game screen with the questions to choose.
"""

###############
### Imports ###
###############

### Python imports ###

import os
import random as rd

### Kivy imports ###

from kivy.clock import Clock
from kivy.properties import (
    ColorProperty,
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_TEXT_FONT
)
from tools.constants import (
    DICT_CONTINENTS,
    LIST_CONTINENTS,
    TEXT,
    TIME_CHANGE_BACKGROUND,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED
)
from tools.kivy_tools import ImprovedScreen

#############
### Class ###
#############


class GameQuestionScreen(ImprovedScreen):

    previous_screen_name = StringProperty()
    code_continent = StringProperty(LIST_CONTINENTS[0])
    continent_color = ColorProperty(DICT_CONTINENTS[LIST_CONTINENTS[0]])
    background_color = ColorProperty(
        DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[LIST_CONTINENTS[0]])
    title_label = StringProperty()
    number_lives_on = NumericProperty(3)
    hint1 = StringProperty()
    hint2 = StringProperty()
    hint3 = StringProperty()
    clue = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + self.code_continent + "/" +
            rd.choice(os.listdir(PATH_BACKGROUNDS + self.code_continent)),
            font_name=PATH_TEXT_FONT,
            **kwargs)

        # The function is called each time code_continent of the class changes
        self.bind(code_continent=self.update_color)
        self.bind(previous_screen_name=self.bind_function)
        self.update_labels()

    def bind_function(self, *args):
        pass

    def on_pre_enter(self, *args):

        # Change the labels
        self.update_labels()

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
            "home").previous_screen_name = "game_question"
        self.manager.current = "home"

    def go_to_game_summary(self, hint):
        self.manager.get_screen(
            "game_summary").previous_screen_name = "game_question"
        self.manager.get_screen(
            "game_summary").current_hint = hint
        self.manager.current = "game_summary"

    def update_labels(self):
        """
        Update the labels depending on the language.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.title_label = TEXT.game_question["title"]
        self.hint1 = TEXT.game_question["hint_1"]
        self.hint2 = TEXT.game_question["hint_2"]
        self.hint3 = TEXT.game_question["hint_3"]
        self.clue = TEXT.game_question["clue"]
