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
    TEXT,
    USER_DATA
)


#############
### Class ###
#############


class HomeScreen(ImprovedScreen):

    counter_continents = 0
    continent_name = StringProperty()
    highscore = StringProperty()
    completion_percentage = StringProperty()
    continent_color = ObjectProperty(LIST_CONTINENTS[counter_continents]["colors"])
    continent_image = StringProperty(
        PATH_CONTINENTS_IMAGES + LIST_CONTINENTS[counter_continents]["name"] + ".png")
    language_image = StringProperty(
        PATH_LANGUAGES_IMAGES + TEXT.language + ".png")
    play_label = StringProperty()

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "lake_sunset.jpg",
            **kwargs)
        self.update_labels()
    
    def update_labels(self):
        code_continent = LIST_CONTINENTS[self.counter_continents]["name"]
        self.continent_name = TEXT.home[code_continent]
        self.play_label = TEXT.home["play"]
        self.highscore = TEXT.home["highscore"] + \
            str(USER_DATA.continents[code_continent]["highscore"])

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
        code_continent = LIST_CONTINENTS[self.counter_continents]["name"]
        self.continent_name = TEXT.home[code_continent]
        self.continent_color = LIST_CONTINENTS[self.counter_continents]["colors"]
        self.continent_image = PATH_CONTINENTS_IMAGES + \
            LIST_CONTINENTS[self.counter_continents]["name"] + ".png"
        
        # Change the score and the completion percentage of the user
        self.highscore = TEXT.home["highscore"] + \
            str(USER_DATA.continents[code_continent]["highscore"])
        self.completion_percentage = str(USER_DATA.continents[code_continent]["percentage"]) + " %"

    def change_language(self):
        # Change the language in the text
        if TEXT.language == "english":
            TEXT.change_language("french")
        else:
            TEXT.change_language("english")
        self.update_labels()
        
        # Save the choice of the language
        USER_DATA.language = TEXT.language
        USER_DATA.save_changes()

        # Change the language icon
        self.language_image = PATH_LANGUAGES_IMAGES + TEXT.language + ".png"

    def play_game(self):
        self.manager.current = "game_question"
