"""
Module to create the game screen with the questions to choose.
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
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    SCREEN_ICON_LEFT_UP,
    SCREEN_TITLE,
    SCREEN_MULTIPLIER,
    SCREEN_THREE_LIVES,
    SCREEN_CONTINENT_PROGRESS_BAR,
    SCREEN_COUNTRY_STARS,
    SCREEN_NB_CREDITS,
    DICT_HINTS_INFORMATION
)
from tools.geozzle import (
    TEXT,
    USER_DATA,
    SHARED_DATA
)
from screens.custom_widgets import GeozzleScreen, TutorialView, MessagePopup

#############
### Class ###
#############


class GameQuestionScreen(GeozzleScreen):

    title_label = StringProperty()
    list_of_clues_label = StringProperty()
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
        SCREEN_CONTINENT_PROGRESS_BAR: "",
        SCREEN_COUNTRY_STARS: "",
        SCREEN_NB_CREDITS: "",
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=rd.choice(SHARED_DATA.list_unlocked_backgrounds),
            font_name=PATH_TEXT_FONT,
            **kwargs)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        
        # Disable the go to list of clues button if the user has selected no clues
        if len(USER_DATA.game.dict_guessed_countries[USER_DATA.game.current_guess_country]["list_clues"]) == 0:
            self.ids.clue_button.opacity = 0
            self.ids.clue_button.disable_button = True
        else:
            self.ids.clue_button.opacity = 1
            self.ids.clue_button.disable_button = False

    def on_enter(self, *args):
        super().on_enter(*args)

        # Tutorial mode
        if USER_DATA.game.tutorial_mode:
            if USER_DATA.game.detect_tutorial_number_clue(number_clue=0):
                # Add a modal view to allow only hint 3
                TutorialView(widget_to_show=self.ids["hint_3_button"])
                # Display popup with explanations
                popup = MessagePopup(
                    title=TEXT.tutorial["tutorial_title"],
                    primary_color=self.continent_color,
                    secondary_color=self.secondary_continent_color,
                    center_label_text=TEXT.tutorial["int_tutorial_1"],
                    font_ratio=self.font_ratio,
                    ok_button_label=TEXT.popup["close"]
                )
                popup.open()
            if USER_DATA.game.detect_tutorial_number_clue(number_clue=1):
                # Add modal view to allow only hint 2
                TutorialView(widget_to_show=self.ids["hint_2_button"])

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
        self.list_of_clues_label = TEXT.game_question["list_of_clues"]
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

    def add_clue(self, code_clue: str):
        # Add the clue in the class
        USER_DATA.game.ask_clue(code_clue=code_clue)

        # Change screen
        self.go_to_game_summary()

    def go_to_game_summary(self):
        self.manager.get_screen(
            "game_summary").previous_screen_name = "game_question"
        self.manager.current = "game_summary"
