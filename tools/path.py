"""
Module to store all the paths used for the app files and folders
"""
###############
### Imports ###
###############

from kivy.utils import platform
from kivy.app import App

#################
### Constants ###
#################

IOS_MODE = platform == "ios"
ANDROID_MODE = platform == "android"

if ANDROID_MODE:
    from android.storage import app_storage_path  # pylint: disable=import-error # type: ignore
    PATH_APP_FOLDER = app_storage_path() + "/"
elif IOS_MODE:
    my_app = App()
    # PATH_APP_FOLDER = '~/Documents/.%(appname)s.ini/'
    PATH_APP_FOLDER = my_app.user_data_dir
else:
    PATH_APP_FOLDER = "./"

# Path for the folders
PATH_RESOURCES_FOLDER = "resources/"

# Path for the user data
PATH_USER_DATA = PATH_APP_FOLDER + "data.json"

# Path for the screen
PATH_SCREENS = "screens/"

# Path for the resources
PATH_LANGUAGE = PATH_RESOURCES_FOLDER + "languages/"
PATH_IMAGES = PATH_RESOURCES_FOLDER + "images/"
PATH_FLAG_IMAGES = PATH_IMAGES + "flags/"
PATH_MEDALS_IMAGES = PATH_IMAGES + "medals/"
PATH_CONTINENTS_IMAGES = PATH_IMAGES + "continents/"
PATH_LANGUAGES_IMAGES = PATH_IMAGES + "languages/"
PATH_MULTIPLIERS_IMAGES = PATH_IMAGES + "multipliers/"
PATH_NEW_IMAGES = PATH_IMAGES + "new_icons/"
PATH_IMAGES_FLAG = PATH_IMAGES + "flags/"
PATH_BACKGROUNDS = PATH_IMAGES + "backgrounds/"
PATH_STICKERS = PATH_IMAGES + "stickers/"

PATH_SOUNDS = PATH_RESOURCES_FOLDER + "sounds/"
PATH_MUSICS = PATH_RESOURCES_FOLDER + "musics/"
PATH_MAIN_MUSIC = PATH_MUSICS + "world_travel.mp3"
PATH_FONTS = PATH_RESOURCES_FOLDER + "fonts/"
PATH_QUERIES = PATH_RESOURCES_FOLDER + "queries/"
PATH_QUERIES_CONTINENT = PATH_QUERIES + "continents/"
PATH_DICT_EXCEPTIONS_COUNTRIES = PATH_QUERIES_CONTINENT + "exceptions.json"
PATH_DICT_HINTS_INFORMATION = PATH_RESOURCES_FOLDER + "hints_information.json"
PATH_TEMP_IMAGE = PATH_APP_FOLDER + "temp_image.svg"
PATH_IMAGES_FLAG_UNKNOWN = PATH_IMAGES + "flag_unknown.png"
PATH_IMAGES_GEOJSON = PATH_IMAGES + "countries_shape/"
PATH_SECRETS_DICT = PATH_RESOURCES_FOLDER + "secrets.json"

# Path for the fonts
PATH_TEXT_FONT = PATH_FONTS + "Oxanium-Bold.ttf"
PATH_TITLE_FONT = PATH_FONTS + "Oxanium-ExtraBold.ttf"
