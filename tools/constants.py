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
    PATH_QUERIES_CONTINENT,
    PATH_DICT_HINTS_INFORMATION,
    PATH_MULTIPLIERS_IMAGES,
    PATH_NEW_IMAGES,
    PATH_SECRETS_DICT
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)

#################
### Constants ###
#################

### Version ###

__version__ = "2.1.5"


### Debug ###

# SCREENSHOT_SCALE = 2.796
SCREENSHOT_SCALE = 2.732
SCREENSHOT_MODE = False

### Mode ###


DEBUG_MODE = False
FPS = 30
MSAA_LEVEL = 2
BACK_ARROW_SIZE = 0.2

### Database connection ###

SECRETS_DICT = load_json_file(PATH_SECRETS_DICT)
SUPABASE_URL = SECRETS_DICT["supabase_url"]
SUPABASE_API_KEY = SECRETS_DICT["api_key"]

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
    default_user_data = {}
    save_json_file(PATH_USER_DATA, default_user_data)

### Language ###

DICT_LANGUAGE_CODE_TO_NAME = {
    "french": "Français",
    "english": "English"
}
DICT_LANGUAGE_NAME_TO_CODE = {}
for code_language in DICT_LANGUAGE_CODE_TO_NAME:
    DICT_LANGUAGE_NAME_TO_CODE[DICT_LANGUAGE_CODE_TO_NAME[code_language]
                               ] = code_language

LANGUAGES_LIST = tuple(DICT_LANGUAGE_CODE_TO_NAME.values())

### Graphics ###

LOGO_SIZE = 0.14

CUSTOM_BUTTON_BACKGROUND_COLOR = (1, 1, 1, 0.7)
CUSTOM_BUTTON_DISABLE_BACKGROUND_COLOR = (0.7, 0.7, 0.7, 0.7)

OPACITY_ON_BUTTON_PRESS = 0.8
WHITE = (1, 1, 1, 1)
BLACK = (0, 0, 0, 1)
GRAY = (0.8, 0.8, 0.8, 1)
DARK_GRAY = (0.4, 0.4, 0.4, 1)
TRANSPARENT = (0, 0, 0, 0)
TEXT_FONT_COLOR = BLACK
TITLE_OUTLINE_WIDTH = 2
TITLE_OUTLINE_COLOR = (1, 1, 1, 1)
BOTTOM_BAR_HEIGHT = 0.12
SUBTITLE_OUTLINE_WIDTH = 1
TIME_CHANGE_BACKGROUND = 10  # every 10 seconds, the background changes
RATE_CHANGE_OPACITY = 0.03
BUTTON_OUTLINE_WIDTH = 1.5

### Font sizes ###

MAIN_TITLE_FONT_SIZE = 52
TITLE_FONT_SIZE = 33
MAIN_TEXT_FONT_SIZE = 23
MAIN_BUTTON_FONT_SIZE = 20
HIGHSCORE_FONT_SIZE = 23
BUTTON_FONT_SIZE = 17
SPINNER_BUTTON_FONT_SIZE = 19
SUB_TEXT_FONT_SIZE = 19
SMALL_BUTTON_FONT_SIZE = 14
SMALL_SCORE_FONT_SIZE = 13.5

### Ads code ###

REWARD_INTERSTITIAL = "ca-app-pub-2909842258525517/8121987815"
REWARD_AD = "ca-app-pub-2909842258525517/2227010061"
INTERSTITIAL_AD = "ca-app-pub-2909842258525517/7261249864"
NUMBER_CREDITS = 1

### Scores ###

SCORE_GUESSED_COUNTRY = 25

### Gallery ###

PRICE_BACKGROUND = 5000

### Screen ###

SCREEN_TITLE = "screen_title"
SCREEN_ICON_LEFT_UP = "screen_icon_left_up"
SCREEN_ICON_RIGHT_UP = "screen_icon_right_up"
SCREEN_ICON_LEFT_DOWN = "screen_icon_left_down"
SCREEN_ICON_RIGHT_DOWN = "screen_icon_right_down"
SCREEN_THREE_LIVES = "screen_three_lives"
SCREEN_MULTIPLIER = "screen_multiplier"
SCREEN_COUNTRY_STARS = "screen_country_stars"
SCREEN_NB_CREDITS = "screen_nb_credits"
SCREEN_CONTINENT_PROGRESS_BAR = "screen_continent_progress_bar"

DICT_MULTIPLIERS = {
    1.: PATH_MULTIPLIERS_IMAGES + "mult_1-0.png",
    1.2: PATH_MULTIPLIERS_IMAGES + "mult_1-2.png",
    1.4: PATH_MULTIPLIERS_IMAGES + "mult_1-4.png",
    1.6: PATH_MULTIPLIERS_IMAGES + "mult_1-6.png",
    1.8: PATH_MULTIPLIERS_IMAGES + "mult_1-8.png",
    2.: PATH_MULTIPLIERS_IMAGES + "mult_2-0.png"
}
DICT_NEW_IMAGES = {
    0: PATH_NEW_IMAGES + "new-0.png",
    1: PATH_NEW_IMAGES + "new-1.png",
    2: PATH_NEW_IMAGES + "new-2.png",
    3: PATH_NEW_IMAGES + "new-3.png"
}

### Continents ###

LIST_CONTINENTS = ["Europe", "Asia", "Africa",
                   "North_America", "South_America", "Oceania"]
DICT_CONTINENTS_PRIMARY_COLOR = {
    "Europe": (2 / 255, 22 / 255, 117 / 255, 1),
    "Asia": (6 / 255, 79 / 255, 2 / 255, 1),
    "Africa": (177 / 255, 7 / 255, 24 / 255, 1),
    "North_America": (219 / 255, 63 / 255, 0 / 255, 1),
    "South_America": (0 / 255, 130 / 255, 194 / 255, 1),
    "Oceania": (74 / 255, 0 / 255, 149 / 255, 1)
}

DICT_CONTINENT_SECOND_COLOR = {
    "Europe": (209 / 255, 215 / 255, 248 / 255, 1),
    "Asia": (193 / 255, 241 / 255, 195 / 255, 1),
    "Africa": (255 / 255, 215 / 255, 215 / 255, 1),
    "North_America": (246 / 255, 223 / 255, 203 / 255, 1),
    "South_America": (200 / 255, 234 / 255, 239 / 255, 1),
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

### Musics ###

MAIN_MUSIC_NAME = "world_travel"
