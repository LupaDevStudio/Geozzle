"""
Module to create the game screen with the questions to choose.
"""

###############
### Imports ###
###############

### Python imports ###

import os
import random as rd
from functools import partial

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
    DICT_CONTINENTS_PRIMARY_COLOR,
    LIST_CONTINENTS,
    TIME_CHANGE_BACKGROUND,
    DICT_CONTINENT_SECOND_COLOR,
    SCREEN_ICON_LEFT_UP,
    SCREEN_TITLE,
    SCREEN_MULTIPLIER,
    SCREEN_THREE_LIVES,
    SCREEN_CONTINENT_PROGRESS_BAR,
    DICT_HINTS_INFORMATION
)
from tools.geozzle import (
    TEXT,
    USER_DATA,
    SHARED_DATA
)
from screens.custom_widgets import GeozzleScreen

#############
### Class ###
#############


class GameQuestionScreen(GeozzleScreen):

    title_label = StringProperty()
    hint_1 = StringProperty()
    hint_2 = StringProperty()
    hint_3 = StringProperty()
    hint_4 = StringProperty()
    number_stars_1 = NumericProperty(1)
    number_stars_2 = NumericProperty(2)
    number_stars_3 = NumericProperty(3)
    number_stars_4 = NumericProperty(1)
    clue = StringProperty()

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

        # Change the background and propagate it in the other screens
        self.manager.change_background(background_path=PATH_BACKGROUNDS + self.code_continent + "/" + rd.choice(os.listdir(PATH_BACKGROUNDS + self.code_continent)))

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

        # Display the four hints randomly chosen
        code_clue_1 = USER_DATA.game.list_current_clues[0]
        code_clue_2 = USER_DATA.game.list_current_clues[1]
        code_clue_3 = USER_DATA.game.list_current_clues[2]
        code_clue_4 = USER_DATA.game.list_current_clues[3]

        # Display the first clue if it exists
        if not code_clue_1 is None:
            self.title_label = TEXT.game_question["title"]
            self.hint_1 = TEXT.clues[code_clue_1]
            self.number_stars_1 = DICT_HINTS_INFORMATION[code_clue_1]["category"]
            self.ids.hint_1_button.release_function = partial(
                self.add_clue, code_clue_1)
        else:
            self.title_label = TEXT.game_question["no_more_clues"]
            self.hint_1 = TEXT.game_question["go_to_summary"]
            self.ids.hint_1_button.release_function = partial(
                self.add_clue, None)
            self.number_stars_1 = 0

        # Display the second clue if it exists
        if not code_clue_2 is None:
            self.hint_2 = TEXT.clues[code_clue_2]
            self.number_stars_2 = DICT_HINTS_INFORMATION[code_clue_2]["category"]
            self.ids.hint_2_button.release_function = partial(
                self.add_clue, code_clue_2)
            try:
                self.enable_widget("hint_2_button")
            except:
                pass
        else:
            self.hint_2 = ""
            self.disable_widget("hint_2_button")

        # Display the third clue if it exists
        if not code_clue_3 is None:
            self.hint_3 = TEXT.clues[code_clue_3]
            self.number_stars_3 = DICT_HINTS_INFORMATION[code_clue_3]["category"]
            self.ids.hint_3_button.release_function = partial(
                self.add_clue, code_clue_3)
            try:
                self.enable_widget("hint_3_button")
            except:
                pass
        else:
            self.hint_3 = ""
            self.disable_widget("hint_3_button")

        # Display the fourth clue if it exists
        if not code_clue_4 is None:
            self.hint_4 = TEXT.clues[code_clue_4]
            self.number_stars_4 = DICT_HINTS_INFORMATION[code_clue_4]["category"]
            self.ids.hint_4_button.release_function = partial(
                self.add_clue, code_clue_4)
            try:
                self.enable_widget("hint_4_button")
            except:
                pass
        else:
            self.hint_4 = ""
            self.disable_widget("hint_4_button")

        super().reload_language()

    def add_clue(self, code_clue: int):
        # Add the clue in the class
        hint_value = USER_DATA.game.ask_clue(code_clue=code_clue)

        # Change screen
        self.go_to_game_summary(hint_value)

    def go_to_game_summary(self, hint_value: str | None):
        self.manager.get_screen(
            "game_summary").previous_screen_name = "game_question"
        if hint_value is not None:
            self.manager.get_screen(
                "game_summary").current_hint = hint_value
        self.manager.current = "game_summary"
