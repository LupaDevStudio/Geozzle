"""
Module of the main backend of Geozzle.
"""

import random as rd

from tools.constants import (
    USER_DATA,
    MAX_HIGHSCORE,
    TEXT,
    DICT_COUNTRIES
)

from tools.sparql import (
    request_clues
)


def choose_three_clues():
    pass

def calculate_highscore_clues(part_highscore, nb_clues):
    # If the user guesses with less than three clues, he has all points
    if nb_clues <= 4:
        return part_highscore

    # Lose points after
    lost_points = part_highscore * (1-nb_clues/6)
    part_highscore -= lost_points
    if part_highscore <= 0:
        return 0
    return part_highscore


class Game():
    number_lives: int
    number_ads: int
    code_continent: str
    wikidata_code_country: str
    clues: dict
    list_all_countries: list # the list of the wikidata code countries
    list_countries_left: list # the countries left to guess

    def __init__(self):
        pass

    def set_continent(self, continent="Europe"):
        self.code_continent = continent
        self.load_data()

    def load_data(self):
        user_data_continent = USER_DATA.continents[self.code_continent]
        self.clues = user_data_continent["current_country"]["clues"]
        self.number_lives = user_data_continent["current_country"]["nb_lives"]
        self.number_ads = user_data_continent["current_country"]["nb_ads"]

        self.list_all_countries = list(DICT_COUNTRIES[USER_DATA.language][self.code_continent].keys())
        self.list_countries_left = [country for country in self.list_all_countries if not country in user_data_continent["countries_unlocked"]]

        last_country = user_data_continent["current_country"]["country"]
        if user_data_continent["current_country"]["country"] != "":
            self.wikidata_code_country = last_country
        else:
            self.wikidata_code_country = rd.choice(self.list_countries_left)

    def add_clue(self, name_clue):
        
        # Get the code of the clue with its name
        for code_clue in TEXT.clues:
            if code_clue == name_clue:
                break

        value_clue = request_clues(code_clue, self.wikidata_code_country)
        self.clues[code_clue] = value_clue

    def check_country(self, guessed_country:str):
        for wikidata_code_country in DICT_COUNTRIES[USER_DATA.language][self.code_continent]:
            if DICT_COUNTRIES[USER_DATA.language][self.code_continent][wikidata_code_country] == guessed_country:
                break
        print(self.wikidata_code_country)
        print(wikidata_code_country)
        if self.wikidata_code_country == wikidata_code_country:
            return True
        
        # Reduce the number of lives if the user has made a mistake
        self.number_lives -= 1
        return False

    def check_game_over(self):
        if self.number_lives <= 0:
            return True
        return False

    def update_percentage(self):
        percentage = USER_DATA.continents[self.code_continent]["percentage"]
        percentage += 1/len(self.list_all_countries)

        # Save the changes in the USER_DATA
        USER_DATA.continents[self.code_continent]["percentage"] = percentage
        USER_DATA.save_changes()

    def update_highscore(self):
        highscore = USER_DATA.continents[self.code_continent]["highscore"]
        part_highscore = MAX_HIGHSCORE / len(self.list_all_countries)

        # Depending on the number of lives => half the score
        highscore += (self.number_lives*part_highscore)/(2*3)

        # Depending on the number of clues used => the other half of the score
        highscore += calculate_highscore_clues(
            part_highscore=part_highscore/2,
            nb_clues=len(self.clues)
        )
        
        # Save the changes in the USER_DATA
        USER_DATA.continents[self.code_continent]["highscore"] = highscore
        USER_DATA.save_changes()
