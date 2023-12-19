"""
Module to create the home screen.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.properties import (
    StringProperty,
    ObjectProperty
)

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_CONTINENTS_IMAGES,
    PATH_LANGUAGES_IMAGES
)
from tools.kivy_tools import ImprovedScreen
from tools.constants import (
    LIST_CONTINENTS,
    TEXT
)


#############
### Class ###
#############


class HomeScreen(ImprovedScreen):

    counter_continents = 0
    continent_name = StringProperty(LIST_CONTINENTS[counter_continents]["name"])
    highscore = StringProperty("Highscore: 0")
    continent_color = ObjectProperty(LIST_CONTINENTS[counter_continents]["colors"])
    continent_image = StringProperty(
        PATH_CONTINENTS_IMAGES + LIST_CONTINENTS[counter_continents]["name"] + ".png")
    language_image = StringProperty(
        PATH_LANGUAGES_IMAGES + TEXT.language + ".png")

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "lake_sunset.jpg",
            **kwargs)
        print(self.language_image)
    
    def change_continent(self, side):

        # Update the counter
        if side == "left":
            self.counter_continents -= 1
            if self.counter_continents < 0:
                self.counter_continents = len(LIST_CONTINENTS) - 1
        elif side == "right":
            self.counter_continents += 1
            if self.counter_continents >= len(LIST_CONTINENTS):
                self.counter_continents = 0

        # Change the colors and the name of the continent
        continent_code_name = LIST_CONTINENTS[self.counter_continents]["name"]
        self.continent_name = TEXT.home[continent_code_name]
        self.continent_color = LIST_CONTINENTS[self.counter_continents]["colors"]
        self.continent_image = PATH_CONTINENTS_IMAGES + \
            LIST_CONTINENTS[self.counter_continents]["name"] + ".png"

    def change_language(self):
        if TEXT.language == "english":
            TEXT.language = "french"
        else:
            TEXT.language = "english"
        self.language_image = PATH_LANGUAGES_IMAGES + TEXT.language + ".png"

    def play_game(self):
        self.manager.current = "game_question"
