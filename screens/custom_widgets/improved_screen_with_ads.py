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

from kivy.clock import mainthread, Clock
from kivy.properties import (
    StringProperty
)

### Local imports ###

from tools.kivy_tools import ImprovedScreen
from tools.geozzle import AD_CONTAINER
from screens.custom_widgets import (
    TwoButtonsPopup,
    MessagePopup
)

from tools.constants import (
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED,
    SCREEN_ICON_LEFT_DOWN,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP,
    SCREEN_ICON_RIGHT_DOWN,
    SCREEN_ICON_RIGHT_UP,
    BLACK,
    TIME_CHANGE_BACKGROUND
)
from tools.path import (
    PATH_IMAGES
)
from tools.geozzle import (
    USER_DATA,
    TEXT
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
                AD_CONTAINER.watch_ad, partial(self.ad_callback, popup), partial(self.error_ad_loading_message, popup))
            popup.right_release_function = watch_ad_with_callback
            popup.left_button_label = TEXT.popup["close"]
            popup.open()

    @mainthread
    def ad_callback(self, popup: TwoButtonsPopup):
        self.number_lives_on += 1
        USER_DATA.game.add_life()
        popup.dismiss()
        AD_CONTAINER.load_ad()

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

class GeozzleScreen(ImprovedScreenWithAds):
    """
    Improved screen class for Geozzle.
    """

    previous_screen_name = StringProperty()

    # Configuration of the main widgets
    dict_type_screen: dict = {}
    title_screen = StringProperty()

    def __init__(self, back_image_path=None, **kw):
        super().__init__(back_image_path=back_image_path, **kw)

        self.update_dict_type_screen()

    def update_dict_type_screen(self, *args):

        # Display the title or not
        if SCREEN_TITLE in self.dict_type_screen:
            title = self.dict_type_screen[SCREEN_TITLE].get("title", "")
            if title in TEXT.titles:
                self.title_screen = TEXT.titles[title]
            else:
                self.title_screen = title
            self.ids.title.color = self.dict_type_screen[SCREEN_TITLE].get("colors", BLACK)
        else:
            try:
                self.remove_widget(self.ids.title)
            except:
                pass

        # Display the icon in the left up corner
        if SCREEN_ICON_LEFT_UP in self.dict_type_screen:
            dict_details = self.dict_type_screen[SCREEN_ICON_LEFT_UP]
            self.ids.icon_left_up.image_path = PATH_IMAGES + dict_details.get("image_path", "home") + ".png"
            self.ids.icon_left_up.colors = dict_details.get("colors", BLACK)
            self.ids.icon_left_up.release_function = dict_details.get("release_function", self.go_to_home)
        else:
            try:
                self.remove_widget(self.ids.icon_left_up)
            except:
                pass

        # Display the icon in the left down corner
        if SCREEN_ICON_LEFT_DOWN in self.dict_type_screen:
            dict_details = self.dict_type_screen[SCREEN_ICON_LEFT_DOWN]
            self.ids.icon_left_down.image_path = PATH_IMAGES + dict_details.get("image_path", "stats") + ".png"
            self.ids.icon_left_down.colors = dict_details.get("colors", BLACK)
            self.ids.icon_left_down.release_function = dict_details.get("release_function", self.go_to_stats)
        else:
            try:
                self.remove_widget(self.ids.icon_left_down)
            except:
                pass

        # Display the icon in the right up corner
        if SCREEN_ICON_RIGHT_UP in self.dict_type_screen:
            dict_details = self.dict_type_screen[SCREEN_ICON_RIGHT_UP]
            self.ids.icon_right_up.image_path = PATH_IMAGES + dict_details.get("image_path", "settings") + ".png"
            self.ids.icon_right_up.colors = dict_details.get("colors", BLACK)
            self.ids.icon_right_up.release_function = dict_details.get("release_function", self.go_to_settings)
        else:
            try:
                self.remove_widget(self.ids.icon_right_up)
            except:
                pass

        # Display the icon in the right down corner
        if SCREEN_ICON_RIGHT_DOWN in self.dict_type_screen:
            dict_details = self.dict_type_screen[SCREEN_ICON_RIGHT_DOWN]
            self.ids.icon_right_down.image_path = PATH_IMAGES + dict_details.get("image_path", "gallery") + ".png"
            self.ids.icon_right_down.colors = dict_details.get("colors", BLACK)
            self.ids.icon_right_down.release_function = dict_details.get("release_function", self.go_to_gallery)
        else:
            try:
                self.remove_widget(self.ids.icon_right_down)
            except:
                pass

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.reload_language()

    def reload_language(self):
        self.update_dict_type_screen()

    def go_to_home(self):
        self.manager.get_screen("home").previous_screen_name = self.manager.current
        self.manager.current = "home"

    def go_to_stats(self):
        self.manager.get_screen("stats").previous_screen_name = self.manager.current
        self.manager.current = "stats"

    def go_to_settings(self):
        self.manager.get_screen("settings").previous_screen_name = self.manager.current
        self.manager.current = "settings"

    def go_to_gallery(self):
        self.manager.get_screen("gallery").previous_screen_name = self.manager.current
        self.manager.current = "gallery"

        # Unschedule the clock updates
        Clock.unschedule(self.manager.change_background,
            TIME_CHANGE_BACKGROUND)
