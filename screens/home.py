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

from kivy.clock import Clock
from kivy.properties import (
    StringProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_IMAGES,
    ANDROID_MODE,
    IOS_MODE
)
from screens.custom_widgets import GeozzleScreen
from tools.constants import (
    DICT_CONTINENTS_PRIMARY_COLOR,
    TIME_CHANGE_BACKGROUND,
    MAIN_MUSIC_NAME,
    DICT_CONTINENT_SECOND_COLOR,
    SCREEN_ICON_LEFT_DOWN,
    SCREEN_ICON_RIGHT_DOWN,
    SCREEN_ICON_RIGHT_UP,
    BLACK,
    WHITE
)
from tools.geozzle import (
    USER_DATA,
    TEXT,
    SHARED_DATA
)
from tools import (
    music_mixer,
    sound_mixer
)
from screens.custom_widgets import (
    TwoButtonsImagePopup,
    MessagePopup,
    LoadingPopup
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
        if self.previous_screen_name in ["", "gallery", "game_summary", "game_question", "game_over", "stats_continent"]:
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
                    secondary_color=DICT_CONTINENT_SECOND_COLOR[
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

    def prepare_gui_to_play_game(self, has_success: bool, *_):
        if self.loading_popup is not None:
            self.loading_popup.dismiss()
        if has_success:

            try:
                code_continent = USER_DATA.game.current_guess_continent

                self.manager.get_screen(
                    "game_question").code_continent = code_continent
                self.manager.get_screen(
                    "game_summary").reset_scroll_view()
                self.manager.get_screen(
                    "game_summary").code_continent = code_continent
                self.manager.get_screen(
                    "game_over").code_continent = code_continent
                self.manager.get_screen(
                    "game_over").update_countries()

                # Unschedule the clock updates
                Clock.unschedule(self.manager.change_background,
                                TIME_CHANGE_BACKGROUND)

                # Go to the screen game summary if the user has already picked up one clue
                if len(USER_DATA.game.dict_guessed_countries[USER_DATA.game.current_guess_country]["list_clues"]) > 0:
                    next_screen = "game_summary"
                else:
                    next_screen = "game_question"
                self.manager.get_screen(
                    next_screen).previous_screen_name = "home"
                Clock.schedule_once(self.manager.get_screen(
                    next_screen).change_background_continent)
                self.manager.current = next_screen

            # If there is an error in the data
            except:
                USER_DATA.game.reset_all_game_data()
                self.go_to_home()
                popup = MessagePopup(
                    primary_color=self.continent_color,
                    secondary_color=self.secondary_continent_color,
                    title=TEXT.clues["no_connexion_title"],
                    center_label_text=TEXT.clues["no_connexion_message"],
                    ok_button_label=TEXT.popup["close"],
                    font_ratio=self.font_ratio
                )
                popup.open()

        else:
            popup = MessagePopup(
                primary_color=self.continent_color,
                secondary_color=self.secondary_continent_color,
                title=TEXT.clues["no_connexion_title"],
                center_label_text=TEXT.clues["no_connexion_message"],
                ok_button_label=TEXT.popup["close"],
                font_ratio=self.font_ratio
            )
            popup.open()

    def thread_request(self):
        has_success = USER_DATA.game.launch_game()
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
        if not USER_DATA.game.data_already_loaded:
            self.loading_popup = LoadingPopup(
                primary_color=self.continent_color,
                secondary_color=self.secondary_continent_color,
                font_ratio=self.font_ratio)
            self.loading_popup.open()
        else:
            self.loading_popup = None

        # Start thread
        my_thread = Thread(target=self.thread_request)
        my_thread.start()
