"""
Module referencing the main constants of the application.

Constants
---------
__version__ : str
    Version of the application.

MOBILE_MODE : bool
    Whether the application is launched on mobile or not.
"""

###############
### Imports ###
###############

### Python imports ###

import os

### Kivy imports ###

from kivy import platform

### Local imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_LANGUAGE
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

### Version ###

__version__ = "1.0.0"

### Mode ###

MOBILE_MODE = platform == "android"
DEBUG_MODE = False
FPS = 30
MSAA_LEVEL = 2
BACK_ARROW_SIZE = 0.2

### Data loading ###

# Create the user data json if it does not exist
if not os.path.exists(PATH_USER_DATA):
    default_user_data = {
        "language": "english",
        "continents": {
            "Europe": {
                "highscore": 0,
                "percentage": 0,
                "countries_unlocked": [],
                "current_country": {
                    "country": "",
                    "clues": []
                }

            },
            "Asia": {
                "highscore": 0,
                "percentage": 20,
                "countries_unlocked": [],
                "current_country": {
                    "country": "",
                    "clues": []
                }
            },
            "Africa": {
                "highscore": 0,
                "percentage": 30,
                "countries_unlocked": [],
                "current_country": {
                    "country": "",
                    "clues": []
                }
            },
            "North_America": {
                "highscore": 0,
                "percentage": 40,
                "countries_unlocked": [],
                "current_country": {
                    "country": "",
                    "clues": []
                }
            },
            "South_America": {
                "highscore": 0,
                "percentage": 50,
                "countries_unlocked": [],
                "current_country": {
                    "country": "",
                    "clues": []
                }
            },
            "Oceania": {
                "highscore": 0,
                "percentage": 60,
                "countries_unlocked": [],
                "current_country": {
                    "country": "",
                    "clues": []
                }
            }
        }
    }
    save_json_file(PATH_USER_DATA, default_user_data)

# Load the data of the user


class UserData():
    """
    A class to store the user data.
    """

    def __init__(self) -> None:
        data = load_json_file(PATH_USER_DATA)
        self.language = data["language"]
        self.continents = data["continents"]

    def save_changes(self) -> None:
        """
        Save the changes in the data.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Create the dictionary of data
        data = {}
        data["language"] = self.language
        data["continents"] = self.continents

        # Save this dictionary
        save_json_file(
            file_path=PATH_USER_DATA,
            dict_to_save=data)


USER_DATA = UserData()

### Language ###

DICT_LANGUAGE_CORRESPONDANCE = {
    "french": "Français",
    "english": "English"
}
DICT_LANGUAGE_NAME_TO_CODE = {
    "Français": "french",
    "English": "english"
}
LANGUAGES_LIST = tuple(DICT_LANGUAGE_CORRESPONDANCE.values())


class Text():
    def __init__(self, language) -> None:
        self.language = language
        self.change_language(language)

    def change_language(self, language):
        """
        Change the language of the text contained in the class.

        Parameters
        ----------
        language : str
            Code of the desired language.

        Returns
        -------
        None
        """
        # Change the language
        self.language = language

        # Load the json file
        data = load_json_file(PATH_LANGUAGE + language + ".json")

        # Split the text contained in the screens
        self.home = data["home"]
        self.game_question = data["game_question"]
        self.game_summary = data["game_summary"]
        self.game_over = data["game_over"]


TEXT = Text(language=USER_DATA.language)

### Graphics ###

CUSTOM_BUTTON_BACKGROUND_COLOR = (1, 1, 1, 0.7)

OPACITY_ON_BUTTON_PRESS = 0.8

TEXT_FONT_COLOR = (0, 0, 0, 1)
TITLE_OUTLINE_WIDTH = 2
TITLE_OUTLINE_COLOR = (1, 1, 1, 1)
BOTTOM_BAR_HEIGHT = 0.12
SUBTITLE_OUTLINE_WIDTH = 1
TIME_CHANGE_BACKGROUND = 10  # every 10 seconds, the background changes
RATE_CHANGE_OPACITY = 0.03

### Font sizes ###

TITLE_FONT_SIZE = 60
MAIN_TEXT_FONT_SIZE = 30
MAIN_BUTTON_FONT_SIZE = 25
HIGHSCORE_FONT_SIZE = 25
BUTTON_FONT_SIZE = 20
SUB_TEXT_FONT_SIZE = 20

### Ads code ###

REWARD_INTERSTITIAL = ""
INTERSTITIAL = ""

### Continents ###

LIST_CONTINENTS = ["Europe", "Asia", "Africa",
                   "North_America", "South_America", "Oceania"]
DICT_CONTINENTS = {
    "Europe": (2 / 255, 22 / 255, 117 / 255, 1),
    "Asia": (6 / 255, 79 / 255, 2 / 255, 1),
    # "Asia": (0,61/255,4/255,1),

    "Africa": (177 / 255, 7 / 255, 24 / 255, 1),
    "North_America": (219 / 255, 63 / 255, 0 / 255, 1),
    "South_America": (0 / 255, 130 / 255, 194 / 255, 1),
    "Oceania": (74 / 255, 0 / 255, 149 / 255, 1)
}

DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED = {
    "Europe": (209 / 255, 215 / 255, 248 / 255, 1),
    "Asia": (193 / 255, 241 / 255, 195 / 255, 1),
    "Africa": (255 / 255, 215 / 255, 215 / 255, 1),
    "North_America": (253 / 255, 239 / 255, 194 / 255, 1),
    "South_America": (189 / 255, 250 / 255, 246 / 255, 1),
    "Oceania": (226 / 255, 189 / 255, 255 / 255, 1)
}

### Musics ###

MUSIC_VOLUME = 0.5
SOUND_VOLUME = 0.5
MAIN_MUSIC_NAME = "world_travel"
