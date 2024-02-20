"""
Create a class to add the functions to create a screen with an ads popup.
"""

###############
### Imports ###
###############

### Python imports ###

import time
from functools import partial

### Kivy imports ###

from kivy.clock import mainthread

### Local imports ###

from tools.kivy_tools import ImprovedScreen
from tools.geozzle import watch_ad, load_ad
from screens.custom_widgets import (
    TwoButtonsPopup,
    MessagePopup
)

from tools.constants import (
    TEXT,
    USER_DATA,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED
)
from tools import (
    game
)

##############
### Class ####
##############


class ImprovedScreenWithAds(ImprovedScreen):

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
            time_to_next_life = int((15 - diff_time / 60) % 15)
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
                watch_ad, partial(self.ad_callback, popup), partial(self.error_ad_loading_message, popup))
            popup.right_release_function = watch_ad_with_callback
            popup.left_button_label = TEXT.popup["close"]
            popup.open()

    @mainthread
    def ad_callback(self, popup: TwoButtonsPopup):
        self.number_lives_on += 1
        game.add_life()
        popup.dismiss()
        load_ad()

    @mainthread
    def error_ad_loading_message(self, popup: TwoButtonsPopup):
        popup.dismiss()
        error_popup = MessagePopup(
            primary_color=self.continent_color,
            secondary_color=DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[self.code_continent],
            center_label_text=TEXT.clues["no_connexion_message"],
            font_ratio=self.font_ratio,
            title=TEXT.clues["no_connexion_title"])
        error_popup.open()
