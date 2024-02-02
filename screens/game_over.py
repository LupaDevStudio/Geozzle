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
    ColorProperty,
    NumericProperty,
    ListProperty
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
    TEXT,
    DICT_COUNTRIES,
    USER_DATA
)
from tools.kivy_tools import ImprovedScreen
from tools import (
    game
)

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
    congrats_defeat_message = StringProperty()
    validate_label = StringProperty()
    continue_game_label = StringProperty()
    number_lives_on = NumericProperty()
    list_countries = ListProperty([""])

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + self.code_continent + "/" +
            rd.choice(os.listdir(PATH_BACKGROUNDS + self.code_continent)),
            font_name=PATH_TEXT_FONT,
            **kwargs)

        self.bind(code_continent=self.update_color)
        self.update_text()

    def on_pre_enter(self, *args):

        # Change the labels
        self.update_text()

        self.ids.continue_button.opacity = 0

        return super().on_pre_enter(*args)

    def on_enter(self, *args):

        # Update the list of countries
        self.update_countries()

        # Schedule the change of background
        Clock.schedule_interval(
            self.manager.change_background, TIME_CHANGE_BACKGROUND)

        self.number_lives_on = game.number_lives
        self.congrats_defeat_message = ""
        self.ids.continue_button.opacity = 0
        self.ids.continue_button.disable_button = True
        self.ids.validate_button.disable_button = False
        self.ids.validate_button.background_color[-1] = 1

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
        self.congrats_defeat_message = TEXT.game_over["congrats"]
        self.validate_label = TEXT.game_over["validate"]
        self.continue_game_label = TEXT.game_over["continue"]

    def update_countries(self):
        self.list_countries = [""]
        for wikidata_code_country in game.list_countries_left:
            self.list_countries.append(DICT_COUNTRIES[USER_DATA.language][self.code_continent][wikidata_code_country])
        self.list_countries.pop(0)

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

    def go_back_to_summary(self):
        self.manager.get_screen(
            "game_summary").previous_screen_name = "game_over"
        self.manager.current = "game_summary"

    def go_to_next_screen(self):
        if self.continue_game_label in [TEXT.game_over["finish"], TEXT.game_over["button_game_over"]]:
            self.manager.get_screen(
                "home").previous_screen_name = "game_over"
            self.manager.get_screen(
                "home").code_continent = self.code_continent
            self.manager.current = "home"

        elif self.continue_game_label == TEXT.game_over["next_country"]:
            self.manager.get_screen(
                "game_question").previous_screen_name = "game_over"
            self.manager.get_screen(
                "game_question").code_continent = self.code_continent
            # Create a new game
            game.set_continent(self.code_continent)

        elif self.continue_game_label == TEXT.game_over["continue"]:
            self.manager.get_screen(
                "game_question").previous_screen_name = "game_over"
            self.manager.get_screen(
                "game_question").code_continent = self.code_continent
            self.manager.current = "game_question"

    def submit_country(self):
        if self.ids.country_spinner.text != "":
            self.ids.continue_button.opacity = 1
            self.ids.continue_button.disable_button = False
            self.ids.validate_button.disable_button = True
            self.ids.validate_button.background_color[-1] = 0.5

            if game.check_country(self.ids.country_spinner.text):
                # If the continent is finished
                if game.list_countries_left == []:
                    self.continue_game_label = TEXT.game_over["finish"]
                else:
                    self.continue_game_label = TEXT.game_over["next_country"]
                self.congrats_defeat_message = TEXT.game_over["congrats"]
                game.update_highscore()
                game.update_percentage()
            else:
                self.number_lives_on = game.number_lives
                if game.check_game_over():
                    self.continue_game_label = TEXT.game_over["button_game_over"]
                    self.congrats_defeat_message = TEXT.game_over["game_over"]
                else:
                    self.continue_game_label = TEXT.game_over["continue"]
                    self.congrats_defeat_message = TEXT.game_over["defeat"]
