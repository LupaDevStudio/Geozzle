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
    BLACK,
    GRAY,
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
    MessagePopup
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
