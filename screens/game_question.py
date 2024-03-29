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
from kivy.clock import Clock

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
from screens.custom_widgets import ImprovedScreenWithAds
from tools import (
    game
)
from screens.custom_widgets import (
    MessagePopup
)

#############
### Class ###
#############


class GameQuestionScreen(ImprovedScreenWithAds):

    previous_screen_name = StringProperty()
    code_continent = StringProperty(LIST_CONTINENTS[0])
    continent_color = ColorProperty(DICT_CONTINENTS[LIST_CONTINENTS[0]])
    background_color = ColorProperty(
        DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[LIST_CONTINENTS[0]])
    title_label = StringProperty()
    number_lives_on = NumericProperty()
    hint_1 = StringProperty()
    hint_2 = StringProperty()
    hint_3 = StringProperty()
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

    def bind_function(self, *args):
        pass

    def on_enter(self, *args):
        # Change the labels
        self.update_labels()

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

    def add_clue(self, hint):
        # Add the clue in the class
        game.select_clue(hint)

        # Change screen
        self.go_to_game_summary(hint)

    def go_to_game_summary(self, hint):
        self.manager.get_screen(
            "game_summary").previous_screen_name = "game_question"
        if not hint is None:
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
        # Pick randomly three clues
        hint_1, hint_2, hint_3 = game.choose_three_clues()

        # Display the first clue if it exists
        if not hint_1 is None:
            self.title_label = TEXT.game_question["title"]
            self.hint_1 = TEXT.clues[hint_1]
            try:
                self.enable_widget("hint_1_button")
            except:
                pass
        else:
            self.title_label = TEXT.game_question["no_more_clues"]
            self.hint_1 = ""
            self.disable_widget("hint_1_button")

        # Display the second clue if it exists
        if not hint_2 is None:
            self.hint_2 = TEXT.clues[hint_2]
            try:
                self.enable_widget("hint_2_button")
            except:
                pass
        else:
            self.hint_2 = ""
            self.disable_widget("hint_2_button")

        # Display the third clue if it exists
        if not hint_3 is None:
            self.hint_3 = TEXT.clues[hint_3]
            try:
                self.enable_widget("hint_3_button")
            except:
                pass
        else:
            self.hint_3 = ""
            self.disable_widget("hint_3_button")
