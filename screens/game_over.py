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
    PATH_TEXT_FONT,
    PATH_FLAG_IMAGES
)
from tools.constants import (
    DICT_MULTIPLIERS,
    DICT_NEW_IMAGES,
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
    SHARED_DATA,
    get_nb_stars,
    AD_CONTAINER
)
from screens.custom_widgets import GeozzleScreen
from screens.custom_widgets import (
    TwoButtonsPopup,
    MessagePopup,
    LoadingPopup,
    EndCountryPopup
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
    back_label = StringProperty()
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

        self.title_label = TEXT.game_over["title"]
        self.validate_label = TEXT.game_over["validate"]
        self.back_label = TEXT.game_over["button_back"]

        super().reload_language()

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        # Stop the tutorial mode
        if USER_DATA.game.tutorial_mode:
            USER_DATA.game.tutorial_mode = False
        USER_DATA.save_changes()

    def update_countries(self, *_):
        """
        Update the list of countries displayed in the spinner.
        """

        self.ids.country_spinner.text = ""
        self.list_countries = []
        for wikidata_code_country in USER_DATA.game.list_countries_in_spinner:
            self.list_countries.append(DICT_COUNTRIES[
                USER_DATA.language][self.code_continent][wikidata_code_country])

        # Sort the list for alphabetical order
        self.list_countries.sort()

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
            self.manager.get_screen(
                "game_summary").reset_scroll_view()
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
                code_country = USER_DATA.game.current_guess_country
                score, score_game = USER_DATA.game.compute_country_and_game_score()
                nb_stars = get_nb_stars(
                    list_clues=USER_DATA.game.dict_guessed_countries[code_country]["list_clues"])
                is_country_new = USER_DATA.check_country_is_new(
                    code_continent=self.code_continent,
                    code_country=code_country,
                    nb_stars=nb_stars
                )
                current_multiplier = USER_DATA.game.current_multiplier

                # Finish the country
                has_finished_game = USER_DATA.game.finish_country()

                # If the game is finished
                if has_finished_game:
                    # End the game
                    self.finish_game(game_over=False)
                    ok_button_label = TEXT.popup["close"]
                    def score_popup_release_function(): return 1 + 1
                else:
                    ok_button_label = TEXT.game_over["next_continent"]
                    score_popup_release_function = self.go_to_next_screen

                # Format the score label
                text = TEXT.game_over["score_popup_text"].replace(
                    "[SCORE]", str(score)).replace(
                        "[SCORE_GAME]", str(score_game))
                # Get the new image if the country is new
                if is_country_new:
                    new_image = DICT_NEW_IMAGES[nb_stars]
                else:
                    new_image = DICT_NEW_IMAGES[0]
                # Display the popup with the score of the current country
                popup = EndCountryPopup(
                    primary_color=self.continent_color,
                    secondary_color=self.secondary_continent_color,
                    title_color=self.continent_color,
                    title=TEXT.game_over["congrats"],
                    ok_button_label=ok_button_label,
                    score_text=text,
                    font_ratio=self.font_ratio,
                    country_name=DICT_COUNTRIES[TEXT.language][self.code_continent][code_country],
                    flag_image=PATH_FLAG_IMAGES + code_country + ".png",
                    nb_stars=nb_stars,
                    multiplier_image=DICT_MULTIPLIERS[current_multiplier],
                    new_image=new_image,
                    release_function=score_popup_release_function
                )
                popup.open()

            # The country is not correct
            else:
                self.number_lives_on = USER_DATA.game.number_lives
                self.update_multiplier()

                # The user has no more lives but ad credits
                if USER_DATA.game.number_lives <= 0 and USER_DATA.game.number_credits > 0:

                    # Open a popup to propose the user to watch an ad
                    popup = TwoButtonsPopup(
                        primary_color=self.continent_color,
                        secondary_color=self.secondary_continent_color,
                        right_button_label=TEXT.popup["watch_ad"],
                        left_button_label=TEXT.game_over["finish_game"],
                        title=TEXT.game_over["buy_life_title"],
                        center_label_text=TEXT.game_over["buy_life_message"],
                        font_ratio=self.font_ratio
                    )
                    watch_ad_with_callback = partial(
                        AD_CONTAINER.watch_ad, partial(self.ad_callback, popup))
                    popup.right_release_function = watch_ad_with_callback
                    popup.left_release_function = self.finish_game
                    popup.open()

                # Game over
                elif USER_DATA.game.number_lives <= 0 and USER_DATA.game.number_credits <= 0:
                    self.finish_game()

                # When the user has still lives
                else:
                    # Open a popup to say the country was not correct
                    popup = MessagePopup(
                        primary_color=self.continent_color,
                        secondary_color=self.secondary_continent_color,
                        title=TEXT.game_over["wrong_country_title"],
                        ok_button_label=TEXT.popup["close"],
                        center_label_text=TEXT.game_over["wrong_country_text"],
                        font_ratio=self.font_ratio
                    )
                    popup.open()

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

    def finish_game(self, game_over: bool = True):
        # End the game and compute the score
        final_score = USER_DATA.game.end_game()

        # TODO Display the popup with the global score
        popup = MessagePopup(
            primary_color=self.continent_color,
            secondary_color=self.secondary_continent_color,
            title=TEXT.game_over["recaps_title"],
            ok_button_label=TEXT.game_over["go_to_home"],
            center_label_text="SCORE FINAL",
            font_ratio=self.font_ratio,
            release_function=self.go_to_home_and_watch_potentially_an_ad
        )
        popup.open()

        if game_over:
            # Display the game over popup
            popup = MessagePopup(
                primary_color=self.continent_color,
                secondary_color=self.secondary_continent_color,
                title=TEXT.game_over["game_over_title"],
                center_label_text=TEXT.game_over["game_over_text"],
                font_ratio=self.font_ratio,
                ok_button_label=TEXT.popup["close"]
            )
            popup.open()

    def go_to_home_and_watch_potentially_an_ad(self):
        # An ad is displayed randomly at the end of the game, if the user has completed the game to more than 10%
        if rd.random() > 0.6 and USER_DATA.get_total_progress() > 10:
            AD_CONTAINER.watch_ad(ad_callback=self.reload_ad)
        self.go_to_home()

    def reload_ad():
        AD_CONTAINER.load_ad()

    @mainthread
    def ad_callback(self, popup: TwoButtonsPopup):
        USER_DATA.game.watch_ad()
        self.number_lives_on = USER_DATA.game.number_lives
        popup.dismiss()
