"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

import os
import webbrowser
import random as rd

### Kivy imports ###

from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    ColorProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CONTINENTS_IMAGES,
    PATH_LANGUAGES_IMAGES,
    PATH_TEXT_FONT
)

from tools.kivy_tools import (
    ImprovedScreen
)

from tools.constants import (
    LIST_CONTINENTS,
    DICT_CONTINENTS,
    TEXT,
    USER_DATA,
    TIME_CHANGE_BACKGROUND,
    MAIN_MUSIC_NAME
)

from tools import (
    music_mixer
)

#############
### Class ###
#############


class HomeScreen(ImprovedScreen):

    counter_continents = 0
    code_continent = LIST_CONTINENTS[counter_continents]
    continent_name = StringProperty()
    highscore = StringProperty()
    completion_value = NumericProperty()
    completion_percentage_text = StringProperty()
    continent_color = ColorProperty(DICT_CONTINENTS[code_continent])
    continent_image = StringProperty(
        PATH_CONTINENTS_IMAGES + LIST_CONTINENTS[counter_continents] + ".png")
    language_image = StringProperty()
    play_label = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + self.code_continent + "/" +
            rd.choice(os.listdir(PATH_BACKGROUNDS + self.code_continent)),
            font_name=PATH_TEXT_FONT,
            **kwargs)
        self.update_text()
        self.update_language_image()
        self.load_continent_data()

    def on_enter(self, *args):
        if music_mixer.musics[MAIN_MUSIC_NAME].state == "stop":
            music_mixer.play(MAIN_MUSIC_NAME, loop=True)

        # Schedule the change of background
        Clock.schedule_interval(self.manager.change_background, TIME_CHANGE_BACKGROUND)

        return super().on_enter(*args)

    def on_pre_leave(self, *args):

        # Unschedule the clock updates
        Clock.unschedule(self.manager.change_background, TIME_CHANGE_BACKGROUND)

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
        self.continent_name = TEXT.home[self.code_continent]
        self.play_label = TEXT.home["play"]
        self.highscore = TEXT.home["highscore"] + \
            str(USER_DATA.continents[self.code_continent]["highscore"])

    def change_continent(self, side: str):
        """
        Change the continent displayed on the screen.

        Parameters
        ----------
        side : str, can be "left" or "right"
            String which indicates the rotation side.

        Returns
        -------
        None
        """

        # Update the counter
        if side == "left":
            self.counter_continents -= 1
            if self.counter_continents < 0:
                self.counter_continents = len(LIST_CONTINENTS) - 1
        elif side == "right":
            self.counter_continents += 1
            if self.counter_continents >= len(LIST_CONTINENTS):
                self.counter_continents = 0

        self.load_continent_data()
        Clock.unschedule(self.manager.change_background, TIME_CHANGE_BACKGROUND)
        Clock.schedule_interval(self.manager.change_background, TIME_CHANGE_BACKGROUND)
        self.manager.change_background()

    def load_continent_data(self):

        # Change the colors and the name of the continent
        self.code_continent = LIST_CONTINENTS[self.counter_continents]
        self.continent_name = TEXT.home[self.code_continent]
        self.continent_color = DICT_CONTINENTS[self.code_continent]
        self.continent_image = PATH_CONTINENTS_IMAGES + \
            LIST_CONTINENTS[self.counter_continents] + ".png"

        # Change the score and the completion percentage of the user
        self.highscore = TEXT.home["highscore"] + \
            str(USER_DATA.continents[self.code_continent]["highscore"])
        self.completion_value = USER_DATA.continents[self.code_continent]["percentage"]
        self.completion_percentage_text = str(
            USER_DATA.continents[self.code_continent]["percentage"]) + " %"

    def update_language_image(self):
        """
        Update the image of the language on the top right hand corner.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if TEXT.language == "french":
            self.language_image = PATH_LANGUAGES_IMAGES + "english.png"
        else:
            self.language_image = PATH_LANGUAGES_IMAGES + "french.png"

    def change_language(self):
        """
        Change the language of the application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Change the language in the text
        if TEXT.language == "english":
            TEXT.change_language("french")
        else:
            TEXT.change_language("english")
        self.update_text()

        # Save the choice of the language
        USER_DATA.language = TEXT.language
        USER_DATA.save_changes()

        # Change the language icon
        self.update_language_image()

    def play_game(self):
        """
        Start the game for one continent.
        It sets the variables of the games for each screen.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print(self.back_image_opacity, self.back_image_path)
        print(self.second_back_image_opacity, self.second_back_image_path)
        print("plus home")
        # Reset the screen of game_summary
        self.manager.get_screen("game_summary").reset_screen()
        self.manager.get_screen(
            "game_question").code_continent = self.code_continent
        self.manager.get_screen(
            "game_question").previous_screen_name = "home"
        self.manager.get_screen(
            "game_summary").code_continent = self.code_continent
        self.manager.get_screen(
            "game_over").code_continent = self.code_continent

        # Go to the screen game question
        self.manager.current = "game_question"

    def open_lupa_website(self):
        """
        Open LupaDevStudio website.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        webbrowser.open("https://lupadevstudio.com", 2)
