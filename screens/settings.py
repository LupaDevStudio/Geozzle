"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

import webbrowser
import random as rd

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    NumericProperty
)

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from screens.custom_widgets import GeozzleScreen
from tools.constants import (
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP,
    __version__
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
    TutorialPopup,
    MessagePopup,
    BigMessagePopup,
    CloudPopup,
    ImportPopup
)

#############
### Class ###
#############


class SettingsScreen(GeozzleScreen):

    language_label = StringProperty()
    music_volume_label = StringProperty()
    sound_volume_label = StringProperty()
    tutorial_label = StringProperty()
    credits_label = StringProperty()
    version_label = StringProperty()
    code_language = StringProperty(TEXT.language)

    music_volume = NumericProperty(USER_DATA.music_volume)
    sound_volume = NumericProperty(USER_DATA.sound_volume)

    dict_type_screen = {
        SCREEN_TITLE: {
            "title": "settings"
        },
        SCREEN_ICON_LEFT_UP: {}
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=rd.choice(SHARED_DATA.list_unlocked_backgrounds),
            font_name=PATH_TEXT_FONT,
            **kwargs)

        self.ids.sound_slider.bind(value=self.update_sound_volume)
        self.ids.music_slider.bind(value=self.update_music_volume)

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
        self.music_volume_label = TEXT.settings["music"]
        self.sound_volume_label = TEXT.settings["sound"]
        self.language_label = TEXT.settings["language"]
        self.tutorial_label = TEXT.settings["tutorial"]
        self.credits_label = TEXT.settings["credits"]
        self.version_label = TEXT.settings["version"].replace(
            "[VERSION]", __version__)

    def change_language_to_french(self):
        self.change_language(code_language="french")

    def change_language(self, code_language="english"):
        """
        Change the language of the application.

        Parameters
        ----------
        code_language: str, optional (default is "english")
            Code of the new language.

        Returns
        -------
        None
        """
        # Change the language in the text
        self.code_language = code_language
        TEXT.change_language(code_language)
        self.reload_language()

        # Save the choice of the language
        USER_DATA.language = TEXT.language
        USER_DATA.save_changes()

    def update_music_volume(self, widget, value):
        self.music_volume = value
        music_mixer.change_volume(self.music_volume)
        USER_DATA.music_volume = self.music_volume
        USER_DATA.save_changes()

    def update_sound_volume(self, widget, value):
        self.sound_volume = value
        sound_mixer.change_volume(self.sound_volume)
        USER_DATA.sound_volume = self.sound_volume
        USER_DATA.save_changes()

    def launch_tutorial(self):
        popup = TutorialPopup(
            primary_color=self.continent_color,
            secondary_color=self.secondary_continent_color,
            tutorial_content=TEXT.tutorial["tutorial_content"],
            font_ratio=self.font_ratio)
        popup.open()

    def open_credits_popup(self):
        popup = MessagePopup(
            primary_color=self.continent_color,
            secondary_color=self.secondary_continent_color,
            title=TEXT.settings["credits"],
            center_label_text=TEXT.settings["credits_text"],
            font_ratio=self.font_ratio,
            ok_button_label=TEXT.popup["close"],
        )
        popup.open()

    def open_cloud_popup(self):
        popup = CloudPopup(
            primary_color=self.continent_color,
            secondary_color=self.secondary_continent_color,
            title=TEXT.settings["cloud_popup_title"],
            center_label_text=TEXT.settings["cloud_popup_text"],
            font_ratio=self.font_ratio,
            close_button_label=TEXT.popup["close"],
            left_button_label=TEXT.settings["export_button"],
            left_release_function=self.export_data,
            right_button_label=TEXT.settings["import_button"],
            right_release_function=self.open_import_popup,
            unique_id=USER_DATA.db_info["user_id"]
        )
        popup.open()

    def export_data(self):
        bool_success = USER_DATA.push_user_data()
        if bool_success:
            popup = BigMessagePopup(
                primary_color=self.continent_color,
                secondary_color=self.secondary_continent_color,
                title=TEXT.settings["export_success_title"],
                center_label_text=TEXT.settings["export_success_text"].replace(
                    "[USER_ID]", USER_DATA.db_info["user_id"]),
                font_ratio=self.font_ratio,
                ok_button_label=TEXT.popup["close"],
            )
            popup.open()
        else:
            popup = MessagePopup(
                primary_color=self.continent_color,
                secondary_color=self.secondary_continent_color,
                title=TEXT.settings["export_fail_title"],
                center_label_text=TEXT.settings["export_fail_text"],
                font_ratio=self.font_ratio,
                ok_button_label=TEXT.popup["close"],
            )
            popup.open()

    def open_import_popup(self):
        popup = ImportPopup(
            primary_color=self.continent_color,
            secondary_color=self.secondary_continent_color,
            title=TEXT.settings["import_title"],
            right_button_label=TEXT.popup["validate"],
            right_release_function=self.import_data,
            left_button_label=TEXT.popup["cancel"],
            center_label_text=TEXT.settings["import_text"],
            warning_label_text=TEXT.settings["import_warning"],
            font_ratio=self.font_ratio,
            id_hint_text=TEXT.settings["id_hint_text"]
        )
        popup.open()

    def import_data(self, user_id: str):
        bool_success = USER_DATA.pull_user_data(user_id=user_id)
        if bool_success:
            title = TEXT.settings["import_success_title"]
            text = TEXT.settings["import_success_text"].replace(
                "[USER_ID]", USER_DATA.db_info["user_id"])
            self.update_settings_menu_after_import()
        else:
            title = TEXT.settings["import_fail_title"]
            text = TEXT.settings["import_fail_text"]
        popup = MessagePopup(
            primary_color=self.continent_color,
            secondary_color=self.secondary_continent_color,
            title=title,
            center_label_text=text,
            font_ratio=self.font_ratio,
            ok_button_label=TEXT.popup["close"],
        )
        popup.open()

    def update_settings_menu_after_import(self):
        self.change_language(code_language=USER_DATA.language)
        self.music_volume = USER_DATA.music_volume
        self.sound_volume = USER_DATA.sound_volume

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

    def open_sous_sous(self):
        webbrowser.open("https://github.com/sponsors/LupaDevStudio", 2)
