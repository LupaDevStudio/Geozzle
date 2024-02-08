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
import time
from functools import partial

### Kivy imports ###

from kivy.clock import Clock, mainthread
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
    MAIN_MUSIC_NAME,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED,
    LIFE_RELOAD_TIME
)

from tools import (
    music_mixer,
    game
)
from screens.custom_widgets import TutorialPopup, TwoButtonsPopup
from tools.geozzle import (
    watch_ad
)

#############
### Class ###
#############


class HomeScreen(ImprovedScreen):

    previous_screen_name = StringProperty()
    counter_continents = 0
    code_continent = LIST_CONTINENTS[counter_continents]
    continent_name = StringProperty()
    highscore = StringProperty()
    completion_value = NumericProperty()
    completion_percentage_text = StringProperty()
    continent_color = ColorProperty(DICT_CONTINENTS[code_continent])
    continent_image = StringProperty(
        PATH_CONTINENTS_IMAGES + LIST_CONTINENTS[counter_continents] + ".jpg")
    language_image = StringProperty()
    play_label = StringProperty()
    number_lives_on = NumericProperty(3)

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + self.code_continent + "/" +
            rd.choice(os.listdir(PATH_BACKGROUNDS + self.code_continent)),
            font_name=PATH_TEXT_FONT,
            **kwargs)
        self.update_text()
        self.update_language_image()
        self.load_continent_data()

    def on_pre_enter(self, *args):
        self.regenerate_lives()
        self.load_continent_data()

        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        if self.previous_screen_name == "":
            self.manager.propagate_background_on_other_screens()

        if music_mixer.musics[MAIN_MUSIC_NAME].state == "stop":
            music_mixer.play(MAIN_MUSIC_NAME, loop=True)

        # Schedule the change of background
        Clock.schedule_interval(
            self.manager.change_background, TIME_CHANGE_BACKGROUND)
        
        if not USER_DATA.has_seen_tutorial:
            USER_DATA.has_seen_tutorial = True
            USER_DATA.save_changes()
            self.launch_tutorial()

        return super().on_enter(*args)

    def regenerate_lives(self):
        for code_continent in LIST_CONTINENTS:
            current_continent_data = USER_DATA.continents[code_continent]
            if current_continent_data["number_lives"] < 3:
                current_time = time.time()
                diff_time = int(
                    current_time - current_continent_data["lost_live_date"])
                diff_minutes = diff_time // 60
                max_number_lives_to_regenerate = diff_minutes // LIFE_RELOAD_TIME
                max_number_lives_to_regenerate = min(
                    3 - current_continent_data["number_lives"], max_number_lives_to_regenerate)
                current_continent_data["number_lives"] += max_number_lives_to_regenerate
                if current_continent_data["number_lives"] == 3:
                    current_continent_data["lost_live_date"] = None
                else:
                    current_continent_data["lost_live_date"] = current_continent_data["lost_live_date"] + \
                        LIFE_RELOAD_TIME * 60 * max_number_lives_to_regenerate
        USER_DATA.save_changes()
        self.number_lives_on = USER_DATA.continents[self.code_continent]["number_lives"]

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
        Clock.unschedule(self.manager.change_background,
                         TIME_CHANGE_BACKGROUND)
        Clock.schedule_interval(
            self.manager.change_background, TIME_CHANGE_BACKGROUND)
        self.manager.change_background()

    def load_continent_data(self):

        # Change the colors and the name of the continent
        self.code_continent = LIST_CONTINENTS[self.counter_continents]
        self.continent_name = TEXT.home[self.code_continent]
        self.continent_color = DICT_CONTINENTS[self.code_continent]
        self.continent_image = PATH_CONTINENTS_IMAGES + \
            LIST_CONTINENTS[self.counter_continents] + ".jpg"

        # Change the score and the completion percentage of the user
        self.highscore = TEXT.home["highscore"] + \
            str(USER_DATA.continents[self.code_continent]["highscore"])
        self.completion_value = USER_DATA.continents[self.code_continent]["percentage"]
        self.completion_percentage_text = str(
            USER_DATA.continents[self.code_continent]["percentage"]) + " %"

        self.number_lives_on = USER_DATA.continents[self.code_continent]["number_lives"]

        if self.completion_value == 100:
            self.disable_widget("play_button")
            self.disable_widget("three_lives")
        else:
            try:
                self.enable_widget("play_button")
                self.enable_widget("three_lives")
            except:
                pass

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

        if self.number_lives_on > 0:

            # Reset the screen of game_summary
            game.create_new_game(self.code_continent)
            self.manager.get_screen("game_summary").reset_screen()
            self.manager.get_screen(
                "game_question").code_continent = self.code_continent
            self.manager.get_screen(
                "game_question").previous_screen_name = "home"
            self.manager.get_screen(
                "game_summary").code_continent = self.code_continent
            self.manager.get_screen(
                "game_over").code_continent = self.code_continent
            self.manager.get_screen(
                "game_over").update_countries()

            # Go to the screen game question
            self.manager.current = "game_question"

        else:
            popup = TwoButtonsPopup(
                primary_color=self.continent_color,
                secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[self.code_continent],
                right_button_label=TEXT.home["watch_ad"],
                title=TEXT.home["buy_life_title"],
                center_label_text=TEXT.home["buy_life_message"],
                font_ratio=self.font_ratio
            )
            watch_ad_with_callback = partial(
                watch_ad, partial(self.ad_callback, popup))
            popup.right_release_function = watch_ad_with_callback
            popup.open()

    def open_buy_life_popup(self):
        if self.number_lives_on == 3:
            popup_text = TEXT.popup["full_life_text"]
            popup = TwoButtonsPopup(
                primary_color=self.continent_color,
                secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[self.code_continent],
                right_button_label=TEXT.popup["watch_ad"],
                title=TEXT.popup["buy_life_title"],
                center_label_text=popup_text,
                font_ratio=self.font_ratio
            )
            popup.ids.right_button.disabled = True
            popup.ids.right_button.opacity = 0
            popup.left_button_label = TEXT.popup["close"]
            popup.open()
        else:
            current_time = time.time()
            diff_time = int(
                current_time - USER_DATA.continents[self.code_continent]["lost_live_date"])
            time_to_next_life = 15 - diff_time // 60
            popup_text = TEXT.popup["next_life_in"].replace(
                "[TIME]", str(time_to_next_life)) + "\n\n" + TEXT.popup["buy_life_text"]
            popup = TwoButtonsPopup(
                primary_color=self.continent_color,
                secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[self.code_continent],
                right_button_label=TEXT.popup["watch_ad"],
                title=TEXT.popup["buy_life_title"],
                center_label_text=popup_text,
                font_ratio=self.font_ratio
            )
            watch_ad_with_callback = partial(
                watch_ad, partial(self.ad_callback, popup))
            popup.right_release_function = watch_ad_with_callback
            popup.left_button_label = TEXT.popup["close"]
            popup.open()

    @mainthread
    def ad_callback(self, popup: TwoButtonsPopup):
        self.number_lives_on += 1
        USER_DATA.continents[self.code_continent]["number_lives"] += 1
        USER_DATA.save_changes()
        popup.dismiss()

    def launch_tutorial(self):
        popup = TutorialPopup(
            title="Tutorial",
            primary_color=self.continent_color,
            secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[self.code_continent],
            tutorial_content=TEXT.tutorial["tutorial_content"],
            font_ratio=self.font_ratio)
        popup.open()

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
