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

### Module imports ###

from tools.path import (
    PATH_USER_DATA,
    PATH_WORDS_10K,
    PATH_WORDS_34K,
    PATH_WORDS_88K,
    PATH_WORDS_375K,
    PATH_GAMEPLAY,
    PATH_THEMES,
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
        "language":""
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

### Colors ###


class ColorPalette():
    """
    Class to store the colors used in the screens.
    """

    def __init__(self) -> None:
        self.PRIMARY = (0, 0, 0, 1)
        self.SECONDARY = (0, 0, 0, 1)

### Graphics ###


TEXT_FONT_COLOR = (0, 0, 0, 1)
TITLE_FONT_SIZE = 45
TITLE_OUTLINE_WIDTH = 2
TITLE_OUTLINE_COLOR = (1, 1, 1, 1)
BOTTOM_BAR_HEIGHT = 0.12

### Musics ###

SOUND_LIST = []


### Ads code ###

REWARD_INTERSTITIAL = ""
INTERSTITIAL = ""

### Words loading ###


with open(PATH_WORDS_10K) as file:
    ENGLISH_WORDS_10K = []
    for i, line in enumerate(file):
        ENGLISH_WORDS_10K.append(line.replace("\n", ""))

with open(PATH_WORDS_34K) as file:
    ENGLISH_WORDS_34K = []
    for i, line in enumerate(file):
        ENGLISH_WORDS_34K.append(line.replace("\n", ""))

with open(PATH_WORDS_88K) as file:
    ENGLISH_WORDS_88K = []
    for i, line in enumerate(file):
        ENGLISH_WORDS_88K.append(line.replace("\n", ""))

with open(PATH_WORDS_375K) as file:
    ENGLISH_WORDS_375K = []
    for i, line in enumerate(file):
        ENGLISH_WORDS_375K.append(line.replace("\n", ""))

ENGLISH_WORDS_DICTS = {
    "10k": ENGLISH_WORDS_10K,
    "34k": ENGLISH_WORDS_34K,
    "88k": ENGLISH_WORDS_88K,
    "375k": ENGLISH_WORDS_375K
}

### Levels ###

GAMEPLAY_DICT = load_json_file(PATH_GAMEPLAY)
