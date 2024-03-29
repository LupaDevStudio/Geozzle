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
    PATH_BACKGROUNDS,
    PATH_TEXT_FONT
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
from screens.custom_widgets import ImprovedScreenWithAds
from tools import (
    game
)
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


class GameOverScreen(ImprovedScreenWithAds):

    previous_screen_name = StringProperty()
    code_continent = StringProperty(LIST_CONTINENTS[0])
    continent_color = ColorProperty(DICT_CONTINENTS[LIST_CONTINENTS[0]])
    background_color = ColorProperty(
        DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[LIST_CONTINENTS[0]])
    title_label = StringProperty()
    congrats_defeat_message = StringProperty()
    score_label = StringProperty()
    validate_label = StringProperty()
    continue_game_label = StringProperty()
    number_lives_on = NumericProperty()
    list_countries = ListProperty([])

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

        self.number_lives_on = game.number_lives
        self.congrats_defeat_message = ""
        self.score_label = ""
        self.ids.validate_button.disable_button = False
        self.ids.validate_button.background_color[-1] = 1

        return super().on_pre_enter(*args)

    def on_enter(self, *args):

        # Schedule the change of background
        Clock.schedule_interval(
            self.manager.change_background, TIME_CHANGE_BACKGROUND)

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
        self.continue_game_label = TEXT.game_over["button_back"]

    def update_countries(self, *_):
        self.ids.country_spinner.text = ""
        self.list_countries = []
        for wikidata_code_country in game.list_countries_left:
            self.list_countries.append(
                DICT_COUNTRIES[USER_DATA.language][self.code_continent][wikidata_code_country])

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

    def go_to_home_and_dismiss(self, popup):
        popup.dismiss()
        game.reset_data_game_over()
        self.go_to_home()

    def go_to_home(self):
        self.manager.get_screen(
            "home").previous_screen_name = "game_over"
        self.manager.get_screen(
            "home").code_continent = self.code_continent
        self.manager.current = "home"

    def prepare_gui_to_play_game(self, has_success, *_):
        self.loading_popup.dismiss()
        if has_success:

            self.manager.get_screen(
                "game_question").previous_screen_name = "game_over"
            self.manager.get_screen(
                "game_question").code_continent = self.code_continent
            self.manager.get_screen(
                "game_summary").reset_scroll_view()
            self.manager.get_screen(
                "game_summary").update_images()
            self.manager.current = "game_question"
            self.update_countries()

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
        has_success = game.create_new_game(self.code_continent)
        Clock.schedule_once(
            partial(self.prepare_gui_to_play_game, has_success))

    def go_to_next_screen(self):
        if self.continue_game_label == TEXT.game_over["next_country"]:

            # Display the loading popup
            self.loading_popup = LoadingPopup(
                primary_color=self.continent_color,
                secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[
                    self.code_continent],
                font_ratio=self.font_ratio)
            self.loading_popup.open()

            # Start thread
            my_thread = Thread(target=self.thread_request)
            my_thread.start()

        elif self.continue_game_label in [TEXT.game_over["continue"], TEXT.game_over["button_back"]]:
            self.manager.get_screen(
                "game_summary").previous_screen_name = "game_over"
            self.manager.get_screen(
                "game_summary").code_continent = self.code_continent
            self.manager.current = "game_summary"

    def disable_validate_button(self):
        self.ids.validate_button.disable_button = True
        self.ids.validate_button.background_color[-1] = 0.5

    def submit_country(self):
        if self.ids.country_spinner.text != "":

            # Reset the spinner
            submitted_country = self.ids.country_spinner.text
            self.ids.country_spinner.text = ""

            # The selected country is correct
            if game.check_country(submitted_country):
                self.disable_validate_button()

                # If the continent is finished
                if game.list_countries_left == []:
                    popup = MessagePopup(
                        primary_color=self.continent_color,
                        secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[
                            self.code_continent],
                        title=TEXT.game_over["congrats"],
                        ok_button_label=TEXT.game_over["go_to_home"],
                        center_label_text=TEXT.game_over["finish_continent"],
                        font_ratio=self.font_ratio
                    )
                    popup.release_function = partial(
                        self.go_to_home_and_dismiss, popup)
                    popup.open()
                else:
                    self.continue_game_label = TEXT.game_over["next_country"]

                self.congrats_defeat_message = TEXT.game_over["congrats"]
                current_score = game.update_score()
                self.score_label = TEXT.home["highscore"] + \
                    str(int(current_score))
                game.update_percentage()

            # The country is not correct
            else:
                self.number_lives_on = game.number_lives
                self.continue_game_label = TEXT.game_over["continue"]
                self.congrats_defeat_message = TEXT.game_over["defeat"]

                # The user has no more lives
                if game.detect_game_over():

                    popup = TwoButtonsPopup(
                        primary_color=self.continent_color,
                        secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[
                            self.code_continent],
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

        # Popup to ask the user to select a country
        else:
            popup = MessagePopup(
                primary_color=self.continent_color,
                secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[self.code_continent],
                title=TEXT.game_over["select_country_title"],
                center_label_text=TEXT.game_over["select_country_message"],
                font_ratio=self.font_ratio
            )
            popup.open()

    @mainthread
    def ad_callback(self, popup: TwoButtonsPopup):
        game.add_life()
        self.number_lives_on = game.number_lives
        popup.dismiss()
