"""
Module referencing the main constants of the application.

Constants
---------
__version__ : str
    Version of the application.

ANDROID_MODE : bool
    Whether the application is launched on mobile or not.
"""

###############
### Imports ###
###############

### Python imports ###

import os


### Local imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_LANGUAGE,
    PATH_QUERIES_CONTINENT,
    PATH_DICT_HINTS_INFORMATION,
    ANDROID_MODE,
    IOS_MODE
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

### Version ###

__version__ = "1.0.8"

### Mode ###


DEBUG_MODE = False
FPS = 30
MSAA_LEVEL = 2
BACK_ARROW_SIZE = 0.2

### Data loading ###

URL_WIKIDATA = 'https://query.wikidata.org/sparql'
CURRENT_COUNTRY_INIT = {
    "country": "",
    "number_lives_used_game": 0,
    "list_current_hints": [],
    "dict_clues": {
        "french": {},
        "english": {}
    },
    "dict_all_clues": {
        "french": {},
        "english": {}
    }
}
# Create the user data json if it does not exist
if not os.path.exists(PATH_USER_DATA):
    default_user_data = {
        "language": "english",
        "has_seen_tutorial": False,
        "continents": {
            "Europe": {
                "highscore": 0,
                "percentage": 0,
                "countries_unlocked": [],
                "number_lives": 3,
                "number_lives_used_game": 0,
                "lost_live_date": None,
                "current_country": CURRENT_COUNTRY_INIT
            },
            "Asia": {
                "highscore": 0,
                "percentage": 0,
                "countries_unlocked": [],
                "number_lives": 3,
                "number_lives_used_game": 0,
                "lost_live_date": None,
                "current_country": CURRENT_COUNTRY_INIT
            },
            "Africa": {
                "highscore": 0,
                "percentage": 0,
                "countries_unlocked": [],
                "number_lives": 3,
                "number_lives_used_game": 0,
                "lost_live_date": None,
                "current_country": CURRENT_COUNTRY_INIT
            },
            "North_America": {
                "highscore": 0,
                "percentage": 0,
                "countries_unlocked": [],
                "number_lives": 3,
                "number_lives_used_game": 0,
                "lost_live_date": None,
                "current_country": CURRENT_COUNTRY_INIT
            },
            "South_America": {
                "highscore": 0,
                "percentage": 0,
                "countries_unlocked": [],
                "number_lives": 3,
                "number_lives_used_game": 0,
                "lost_live_date": None,
                "current_country": CURRENT_COUNTRY_INIT
            },
            "Oceania": {
                "highscore": 0,
                "percentage": 0,
                "countries_unlocked": [],
                "number_lives": 3,
                "number_lives_used_game": 0,
                "lost_live_date": None,
                "current_country": CURRENT_COUNTRY_INIT
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
        self.has_seen_tutorial = data["has_seen_tutorial"]
        if "has_seen_popup_linconym" not in data:
            self.has_seen_popup_linconym = False
        else:
            self.has_seen_popup_linconym = data["has_seen_popup_linconym"]

    def has_finished_one_continent(self) -> bool:
        for continent_name in self.continents:
            continent = self.continents[continent_name]
            if continent["percentage"] == 100:
                return True
        return False

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
        data["has_seen_tutorial"] = self.has_seen_tutorial
        data["has_seen_popup_linconym"] = self.has_seen_popup_linconym

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
        self.clues = data["clues"]
        self.tutorial = data["tutorial"]
        self.popup = data["popup"]


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
BUTTON_OUTLINE_WIDTH = 1.5

### Font sizes ###

TITLE_FONT_SIZE = 60
MAIN_TEXT_FONT_SIZE = 30
MAIN_BUTTON_FONT_SIZE = 22
HIGHSCORE_FONT_SIZE = 25
BUTTON_FONT_SIZE = 18
SPINNER_BUTTON_FONT_SIZE = 20
SUB_TEXT_FONT_SIZE = 20
SMALL_BUTTON_FONT_SIZE = 15

### Ads code ###

REWARD_INTERSTITIAL = "ca-app-pub-2909842258525517/8121987815"

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

DICT_WIKIDATA_CONTINENTS = {
    "Europe": "Q46",
    "Asia": "Q48",
    "Africa": "Q15",
    "North_America": "Q49",
    "South_America": "Q18",
    "Oceania": "Q55643"
}

DICT_WIKIDATA_LANGUAGE = {
    "english": "en",
    "french": "fr"
}

DICT_COUNTRIES = {
    "english": {
        "Europe": load_json_file(PATH_QUERIES_CONTINENT + "Europe_en.json"),
        "Asia": load_json_file(PATH_QUERIES_CONTINENT + "Asia_en.json"),
        "Africa": load_json_file(PATH_QUERIES_CONTINENT + "Africa_en.json"),
        "North_America": load_json_file(PATH_QUERIES_CONTINENT + "North_America_en.json"),
        "South_America": load_json_file(PATH_QUERIES_CONTINENT + "South_America_en.json"),
        "Oceania": load_json_file(PATH_QUERIES_CONTINENT + "Oceania_en.json")
    },
    "french": {
        "Europe": load_json_file(PATH_QUERIES_CONTINENT + "Europe_fr.json"),
        "Asia": load_json_file(PATH_QUERIES_CONTINENT + "Asia_fr.json"),
        "Africa": load_json_file(PATH_QUERIES_CONTINENT + "Africa_fr.json"),
        "North_America": load_json_file(PATH_QUERIES_CONTINENT + "North_America_fr.json"),
        "South_America": load_json_file(PATH_QUERIES_CONTINENT + "South_America_fr.json"),
        "Oceania": load_json_file(PATH_QUERIES_CONTINENT + "Oceania_fr.json")
    }
}

DICT_HINTS_INFORMATION = load_json_file(file_path=PATH_DICT_HINTS_INFORMATION)
LIST_CLUES_EXCEPTIONS = ["ISO_2_code"]

### Gameplay ###

MAX_HIGHSCORE = 10000
LIFE_RELOAD_TIME = 15

### Musics ###

MUSIC_VOLUME = 0.5
SOUND_VOLUME = 1
MAIN_MUSIC_NAME = "world_travel"
