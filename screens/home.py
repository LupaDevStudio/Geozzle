"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd
from functools import partial
from threading import Thread

### Kivy imports ###

from kivy.clock import Clock, mainthread
from kivy.properties import (
    StringProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_MEDALS_IMAGES
)
from screens.custom_widgets import (
    GeozzleScreen
)
from tools.constants import (
    TIME_CHANGE_BACKGROUND,
    MAIN_MUSIC_NAME,
    DICT_MEDALS,
    SCREEN_ICON_LEFT_DOWN,
    SCREEN_ICON_RIGHT_DOWN,
    SCREEN_ICON_RIGHT_UP
)
from tools.geozzle import (
    USER_DATA,
    TEXT,
    SHARED_DATA
)
from tools import (
    music_mixer
)
from screens.custom_widgets import (
    MessagePopup,
    LoadingPopup
)

#############
### Class ###
#############


class HomeScreen(GeozzleScreen):

    highscore_label = StringProperty()
    play_label = StringProperty()
    ranking_label = StringProperty()

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

        self.ids.world_ranking_button.disable_button = True
        ranking_update_thread = Thread(target=self.update_ranking)
        ranking_update_thread.start()

    @mainthread
    def update_ranking_display(self, *args):
        if USER_DATA.db_info["ranking"] is None:
            self.ranking_label = ""
            self.ids.medal_rank.source = PATH_MEDALS_IMAGES + "no_medal.png"
        else:
            self.ranking_label = TEXT.home["ranking"].replace(
                "[RANK]", str(USER_DATA.db_info["ranking"]))
            if USER_DATA.db_info["ranking"] <= 3:
                self.ids.medal_rank.source = DICT_MEDALS[USER_DATA.db_info["ranking"]]
            else:
                self.ids.medal_rank.source = PATH_MEDALS_IMAGES + "no_medal.png"

    def update_ranking(self, *args):
        # Get the world ranking of the user
        USER_DATA.update_world_ranking()
        Clock.schedule_once(self.update_ranking_display)

        # Enable the button when the pull request is over
        self.ids.world_ranking_button.disable_button = False

    def on_enter(self, *args):
        super().on_enter(*args)

        if self.previous_screen_name == "":
            self.manager.propagate_background_on_other_screens()

        if music_mixer.musics[MAIN_MUSIC_NAME].state == "stop":
            music_mixer.play(MAIN_MUSIC_NAME, loop=True)

        # Schedule the change of background
        if self.previous_screen_name in ["", "gallery", "game_summary", "game_question", "game_over", "stats_continent", "world_ranking"]:
            Clock.schedule_interval(
                self.manager.change_background, TIME_CHANGE_BACKGROUND)

        # if USER_DATA.has_finished_one_continent() and not USER_DATA.has_seen_popup_linconym:
        #     popup = TwoButtonsImagePopup(
        #         title="Linconym, the new game of LupaDevStudio",
        #         center_label_text="LupaDevStudio is pleased to present you its new game!\n\nDiscover Linconym, a letter game where your goal is to link words together by rearranging letters to form new ones.",
        #         image_source=PATH_IMAGES + "linconym_banner.png",
        #         left_button_label="Cancel",
        #         right_button_label="Discover",
        #         font_ratio=self.font_ratio,
        #         primary_color=self.continent_color,
        #         secondary_color=DICT_CONTINENT_SECOND_COLOR[
        #             self.code_continent],
        #     )
        #     popup.right_release_function = partial(
        #         self.go_to_linconym, popup)
        #     USER_DATA.has_seen_popup_linconym = True
        #     USER_DATA.save_changes()
        #     popup.open()

    # def go_to_linconym(self, popup: TwoButtonsImagePopup):
    #     popup.dismiss()
    #     if ANDROID_MODE:
    #         webbrowser.open(
    #             "https://play.google.com/store/apps/details?id=lupadevstudio.com.linconym&pli=1", 2)
    #     elif IOS_MODE:
    #         webbrowser.open(
    #             "https://apps.apple.com/app/linconym/id6503208610", 2)

    def go_to_world_ranking(self):
        Clock.unschedule(self.manager.change_background,
            TIME_CHANGE_BACKGROUND)
        self.manager.get_screen(
            "world_ranking").previous_screen_name = self.manager.current
        self.manager.current = "world_ranking"

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
