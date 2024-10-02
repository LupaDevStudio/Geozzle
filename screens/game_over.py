"""
Module to create the game over screen.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd
import os
from functools import partial
from threading import Thread

### Kivy imports ###

from kivy.clock import Clock, mainthread
from kivy.properties import (
    StringProperty,
    ColorProperty,
    NumericProperty,
    ListProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from tools.constants import (
    DICT_CONTINENT_SECOND_COLOR,
    DICT_COUNTRIES,
    SCREEN_ICON_LEFT_UP,
    SCREEN_TITLE,
    SCREEN_MULTIPLIER,
    SCREEN_THREE_LIVES,
    SCREEN_CONTINENT_PROGRESS_BAR
)
from tools.geozzle import (
    TEXT,
    USER_DATA,
    SHARED_DATA
)
from screens.custom_widgets import GeozzleScreen
from screens.custom_widgets import (
    TwoButtonsPopup,
    MessagePopup,
    LoadingPopup
)
from tools.geozzle import (
    AD_CONTAINER
)

#############
### Class ###
#############


class GameOverScreen(GeozzleScreen):

    title_label = StringProperty()
    validate_label = StringProperty()
    continue_game_label = StringProperty()
    list_countries = ListProperty([])

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

        self.validate_label = TEXT.game_over["validate"]
        self.continue_game_label = TEXT.game_over["button_back"]

        super().reload_language()

    def update_countries(self, *_):
        """
        Update the list of countries displayed in the spinner.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.ids.country_spinner.text = ""
        self.list_countries = []
        for wikidata_code_country in USER_DATA.game.list_countries_in_spinner:
            self.list_countries.append(DICT_COUNTRIES[
                USER_DATA.language][self.code_continent][wikidata_code_country])

    def go_back_to_summary(self):
        self.manager.get_screen(
            "game_summary").previous_screen_name = "game_over"
        self.manager.current = "game_summary"

    def prepare_gui_to_play_game(self, has_success, *_):
        self.loading_popup.dismiss()
        if has_success:
            self.code_continent = USER_DATA.game.current_guess_continent

            self.manager.get_screen(
                "game_question").previous_screen_name = "game_over"
            self.manager.get_screen(
                "game_question").code_continent = self.code_continent
            self.manager.get_screen(
                "game_summary").code_continent = self.code_continent
            self.update_countries()

            Clock.schedule_once(self.manager.get_screen(
                "game_question").change_background_continent)
            self.manager.current = "game_question"

        # If no connexion, display a popup and go to home
        else:
            popup = MessagePopup(
                primary_color=self.continent_color,
                secondary_color=self.secondary_continent_color,
                title=TEXT.clues["no_connexion_title"],
                center_label_text=TEXT.clues["no_connexion_message"],
                font_ratio=self.font_ratio,
                ok_button_label=TEXT.popup["close"],
                release_function=self.go_to_home
            )
            popup.open()

    def thread_request(self):
        has_success = USER_DATA.game.go_to_next_country()
        Clock.schedule_once(
            partial(self.prepare_gui_to_play_game, has_success))

    def go_to_next_screen(self):
        # Display the loading popup
        self.loading_popup = LoadingPopup(
            primary_color=self.continent_color,
            secondary_color=self.secondary_continent_color,
            font_ratio=self.font_ratio)
        self.loading_popup.open()

        # Start thread
        my_thread = Thread(target=self.thread_request)
        my_thread.start()

    def submit_country(self):
        if self.ids.country_spinner.text != "":

            # Reset the spinner
            submitted_country = self.ids.country_spinner.text
            self.ids.country_spinner.text = ""

            # The selected country is correct
            if USER_DATA.game.check_country(submitted_country):
                # Compute the score of the current country
                score = USER_DATA.game.compute_country_score()

                # Finish the country
                has_finished_game = USER_DATA.game.finish_country()

                # If the game is finished
                if has_finished_game:
                    # End the game and compute the score
                    final_score = USER_DATA.game.end_game()
                    # TODO display the score popup
                    popup = MessagePopup(
                        primary_color=self.continent_color,
                        secondary_color=self.secondary_continent_color,
                        title=TEXT.game_over["congrats"],
                        ok_button_label=TEXT.game_over["go_to_home"],
                        center_label_text=TEXT.game_over["finish_continent"],
                        font_ratio=self.font_ratio,
                        release_function=self.go_to_home
                    )
                    popup.open()
                    score_popup_release_function = lambda: 1 + 1
                else:
                    self.continue_game_label = TEXT.game_over["next_country"]
                    score_popup_release_function = self.go_to_next_screen

                # Display the popup with the score of the current country
                # TODO changer la popup pour mettre la bonne
                popup = MessagePopup(
                    primary_color=self.continent_color,
                    secondary_color=self.secondary_continent_color,
                    title=TEXT.game_over["congrats"],
                    ok_button_label=TEXT.popup["close"],
                    center_label_text=f"AFFICHER LE SCORE DU PAYS EN COURS {score}",
                    font_ratio=self.font_ratio,
                    release_function=score_popup_release_function
                )

            # The country is not correct
            else:
                self.number_lives_on = USER_DATA.game.number_lives
                # TODO open a popup to say the country was not correct

                # The user has no more lives but ad credits
                if USER_DATA.game.number_lives == 0 and USER_DATA.game.number_credits > 0:

                    popup = TwoButtonsPopup(
                        primary_color=self.continent_color,
                        secondary_color=self.secondary_continent_color,
                        right_button_label=TEXT.home["watch_ad"],
                        left_button_label=TEXT.game_over["go_to_home"],
                        title=TEXT.home["buy_life_title"],
                        center_label_text=TEXT.home["buy_life_message"],
                        font_ratio=self.font_ratio
                    )
                    watch_ad_with_callback = partial(
                        AD_CONTAINER.watch_ad, partial(self.ad_callback, popup))
                    popup.right_release_function = watch_ad_with_callback
                    popup.left_release_function = partial(
                        self.go_to_home_and_dismiss, popup)
                    popup.open()

                # Game over 
                elif USER_DATA.game.number_lives == 0 and USER_DATA.game.number_credits == 0:
                    score = USER_DATA.game.end_game()
                    # TODO display popup global score
                    # TODO display popup game over

        # Popup to ask the user to select a country
        else:
            popup = MessagePopup(
                primary_color=self.continent_color,
                secondary_color=self.secondary_continent_color,
                title=TEXT.game_over["select_country_title"],
                center_label_text=TEXT.game_over["select_country_message"],
                font_ratio=self.font_ratio,
                ok_button_label=TEXT.popup["close"]
            )
            popup.open()

    @mainthread
    def ad_callback(self, popup: TwoButtonsPopup):
        USER_DATA.game.watch_ad()
        self.number_lives_on = USER_DATA.game.number_lives
        popup.dismiss()
