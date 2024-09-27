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
    ColorProperty,
    NumericProperty,
    BooleanProperty
)

### Local imports ###

from tools.path import (
    PATH_LANGUAGES_IMAGES,
    PATH_TEXT_FONT
)
from screens.custom_widgets import GeozzleScreen
from tools.constants import (
    BLACK,
    GRAY,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP
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
    TwoButtonsPopup,
    TwoButtonsImagePopup,
    MessagePopup,
    LoadingPopup,
)

#############
### Class ###
#############


class SettingsScreen(GeozzleScreen):

    music_volume_label = StringProperty()
    sound_volume_label = StringProperty()
    language_label = StringProperty()
    tutorial_label = StringProperty()
    credits_label = StringProperty()
    code_language = StringProperty(TEXT.language)

    dict_type_screen = {
        SCREEN_TITLE: "settings",
        SCREEN_ICON_LEFT_UP: {}
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=rd.choice(SHARED_DATA.list_unlocked_backgrounds),
            font_name=PATH_TEXT_FONT,
            **kwargs)

        self.reload_language()

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

    def change_language_to_french(self):
        self.change_language(code_language="french")

    def change_language(self, code_language="english"):
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
        self.code_language = code_language
        TEXT.change_language(code_language)
        self.reload_language()

        # Save the choice of the language
        USER_DATA.language = TEXT.language
        USER_DATA.save_changes()

    def launch_tutorial(self):
        popup = TutorialPopup(
            primary_color=BLACK,
            secondary_color=GRAY,
            tutorial_content=TEXT.tutorial["tutorial_content"],
            font_ratio=self.font_ratio)
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
