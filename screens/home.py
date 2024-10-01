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
import copy
from threading import Thread

### Kivy imports ###

from kivy.clock import Clock, mainthread
from kivy.properties import (
    StringProperty,
    ColorProperty,
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CONTINENTS_IMAGES,
    PATH_LANGUAGES_IMAGES,
    PATH_TEXT_FONT,
    PATH_IMAGES
)
from screens.custom_widgets import GeozzleScreen
from tools.constants import (
    LIST_CONTINENTS,
    DICT_CONTINENTS,
    TIME_CHANGE_BACKGROUND,
    MAIN_MUSIC_NAME,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED,
    LIFE_RELOAD_TIME,
    CURRENT_COUNTRY_INIT,
    MUSIC_VOLUME,
    SOUND_VOLUME,
    ANDROID_MODE,
    IOS_MODE,
    SCREEN_ICON_LEFT_DOWN,
    SCREEN_ICON_RIGHT_DOWN,
    SCREEN_ICON_RIGHT_UP
)
from tools.geozzle import (
    USER_DATA,
    TEXT,
    AD_CONTAINER,
    SHARED_DATA
)
from tools import (
    music_mixer,
    sound_mixer
)
from screens.custom_widgets import (
    TutorialPopup,
    TwoButtonsPopup,
    TwoButtonsImagePopup,
    MessagePopup,
    LoadingPopup,
)

#############
### Class ###
#############


class HomeScreen(GeozzleScreen):

    highscore_label = StringProperty()
    play_label = StringProperty()

    dict_type_screen = {
        SCREEN_ICON_LEFT_DOWN: {},
        SCREEN_ICON_RIGHT_DOWN: {},
        SCREEN_ICON_RIGHT_UP: {}
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=rd.choice(SHARED_DATA.list_unlocked_backgrounds),
            font_name=PATH_TEXT_FONT,
            **kwargs)

    def on_pre_enter(self, *args):
        # TODO uncomment when fixed in the backend
        # self.regenerate_lives()

        return super().on_pre_enter(*args)

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
        super().reload_language()
        self.play_label = TEXT.home["play"]
        self.highscore_label = TEXT.home["highscore"] + \
            str(USER_DATA.highscore)

    def on_enter(self, *args):
        if self.previous_screen_name == "":
            self.manager.propagate_background_on_other_screens()

        if music_mixer.musics[MAIN_MUSIC_NAME].state == "stop":
            music_mixer.play(MAIN_MUSIC_NAME, loop=True)

        # Schedule the change of background
        if self.previous_screen_name in ["", "gallery", "game_summary", "game_question", "game_over"]:
            Clock.schedule_interval(
                self.manager.change_background, TIME_CHANGE_BACKGROUND)

        # Maybe one day we'll use again this popup to present our next game
        if False:
            if USER_DATA.has_finished_one_continent() and not USER_DATA.has_seen_popup_linconym:
                popup = TwoButtonsImagePopup(
                    title="Linconym, the new game of LupaDevStudio",
                    center_label_text="LupaDevStudio is pleased to present you its new game!\n\nDiscover Linconym, a letter game where your goal is to link words together by rearranging letters to form new ones.",
                    image_source=PATH_IMAGES + "linconym_banner.png",
                    left_button_label="Cancel",
                    right_button_label="Discover",
                    font_ratio=self.font_ratio,
                    primary_color=self.continent_color,
                    secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[
                        self.code_continent],
                )
                popup.right_release_function = partial(
                    self.go_to_linconym, popup)
                USER_DATA.has_seen_popup_linconym = True
                USER_DATA.save_changes()
                popup.open()

        return super().on_enter(*args)

    def go_to_linconym(self, popup: TwoButtonsImagePopup):
        popup.dismiss()
        if ANDROID_MODE:
            webbrowser.open(
                "https://play.google.com/store/apps/details?id=lupadevstudio.com.linconym&pli=1", 2)
        elif IOS_MODE:
            webbrowser.open(
                "https://apps.apple.com/app/linconym/id6503208610", 2)

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
        self.reload_language()

        # Save the choice of the language
        USER_DATA.language = TEXT.language
        USER_DATA.save_changes()

        # Change the language icon
        self.update_language_image()

    def prepare_gui_to_play_game(self, has_success, *_):
        if self.loading_popup is not None:
            self.loading_popup.dismiss()
        if has_success:
            Clock.schedule_once(
                self.manager.get_screen("game_summary").reset_scroll_view
            )

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

            # Unschedule the clock updates
            Clock.unschedule(self.manager.change_background,
                             TIME_CHANGE_BACKGROUND)

        else:
            popup = MessagePopup(
                primary_color=self.continent_color,
                secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[
                    self.code_continent],
                title=TEXT.clues["no_connexion_title"],
                center_label_text=TEXT.clues["no_connexion_message"],
                font_ratio=self.font_ratio
            )
            popup.open()

    def thread_request(self):
        has_success = USER_DATA.game.create_new_game(self.code_continent)
        Clock.schedule_once(
            partial(self.prepare_gui_to_play_game, has_success))

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

        # Display the loading popup
        if not USER_DATA.game.is_already_loaded():
            self.loading_popup = LoadingPopup(
                primary_color=self.continent_color,
                secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[
                    self.code_continent],
                font_ratio=self.font_ratio)
            self.loading_popup.open()
        else:
            self.loading_popup = None

        # Start thread
        my_thread = Thread(target=self.thread_request)
        my_thread.start()

        # else:
        #     popup = TwoButtonsPopup(
        #         primary_color=self.continent_color,
        #         secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[self.code_continent],
        #         right_button_label=TEXT.home["watch_ad"],
        #         title=TEXT.home["buy_life_title"],
        #         center_label_text=TEXT.home["buy_life_message"],
        #         font_ratio=self.font_ratio
        #     )
        #     watch_ad_with_callback = partial(
        #         AD_CONTAINER.watch_ad, partial(self.ad_callback, popup))
        #     popup.right_release_function = watch_ad_with_callback
        #     popup.open()
