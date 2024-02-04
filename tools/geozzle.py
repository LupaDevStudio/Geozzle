"""
Module of the main backend of Geozzle.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd
import time

### Local imports ###

from tools.constants import (
    USER_DATA,
    MAX_HIGHSCORE,
    TEXT,
    DICT_COUNTRIES,
    DICT_HINTS_INFORMATION
)

from tools.sparql import (
    request_clues
)

#################
### Functions ###
#################


def calculate_highscore_clues(part_highscore, nb_clues):
    # If the user guesses with less than three clues, he has all points
    if nb_clues <= 4:
        return int(part_highscore)

    # Lose points after
    lost_points = part_highscore * (1 - nb_clues / 6)
    part_highscore -= lost_points
    if part_highscore <= 0:
        return 0
    return int(part_highscore)


#############
### Class ###
#############

class Game():
    number_lives: int
    code_continent: str
    wikidata_code_country: str
    clues: dict
    # The list of the wikidata code countries
    list_all_countries: list
    # The countries left to guess (wikidata code countries)
    list_countries_left: list

    def __init__(self):
        pass

    def set_continent(self, continent="Europe"):
        self.code_continent = continent
        self.load_data()

    def load_data(self):
        user_data_continent = USER_DATA.continents[self.code_continent]
        self.clues = user_data_continent["current_country"]["clues"]
        self.number_lives = user_data_continent["nb_lives"]

        self.list_all_countries = list(
            DICT_COUNTRIES[USER_DATA.language][self.code_continent].keys())
        self.list_countries_left = [
            country for country in self.list_all_countries if not country in user_data_continent["countries_unlocked"]]

        last_country = user_data_continent["current_country"]["country"]
        if user_data_continent["current_country"]["country"] != "":
            self.wikidata_code_country = last_country
        else:
            self.wikidata_code_country = rd.choice(self.list_countries_left)

    def add_clue(self, name_clue):

        # Get the code of the clue with its name
        for code_clue in TEXT.clues:
            if TEXT.clues[code_clue] == name_clue:
                break

        value_clue = request_clues(code_clue, self.wikidata_code_country)
        self.clues[code_clue] = value_clue

    def check_country(self, guessed_country: str):
        for wikidata_code_country in DICT_COUNTRIES[USER_DATA.language][self.code_continent]:
            if DICT_COUNTRIES[USER_DATA.language][self.code_continent][wikidata_code_country] == guessed_country:
                break
        if self.wikidata_code_country == wikidata_code_country:
            USER_DATA.continents[self.code_continent]["countries_unlocked"].append(
                wikidata_code_country)
            return True

        # Reduce the number of lives if the user has made a mistake
        self.number_lives -= 1
        USER_DATA.continents[self.code_continent]["nb_lives"] = self.number_lives
        if USER_DATA.continents[self.code_continent]["lost_live_date"] is None:
            USER_DATA.continents[self.code_continent]["lost_live_date"] = time.time(
            )
        USER_DATA.save_changes()
        return False

    def check_game_over(self):
        if self.number_lives <= 0:
            return True
        return False

    def update_percentage(self):
        # 100% of completion when the continent is over
        if self.list_countries_left == []:
            percentage = 100
        
        else:
            percentage = USER_DATA.continents[self.code_continent]["percentage"]
            percentage += 100 / len(self.list_all_countries)

        # Save the changes in the USER_DATA
        USER_DATA.continents[self.code_continent]["percentage"] = percentage
        USER_DATA.save_changes()

    def update_highscore(self):
        highscore = USER_DATA.continents[self.code_continent]["highscore"]
        part_highscore = MAX_HIGHSCORE / len(self.list_all_countries)

        # Depending on the number of lives => half the score
        highscore += int((self.number_lives * part_highscore) / (2 * 3))

        # Depending on the number of clues used => the other half of the score
        highscore += calculate_highscore_clues(
            part_highscore=part_highscore / 2,
            nb_clues=len(self.clues)
        )

        # Save the changes in the USER_DATA
        USER_DATA.continents[self.code_continent]["highscore"] = highscore
        USER_DATA.save_changes()

    def choose_three_clues(self):
        """
        Choose three new clues given their probability to appear.

        Parameters
        ----------
        None

        Returns
        -------
        (str, str, str)
            Tuple of the three types of clues.
        """
        dict_probabilities = {}
        hint_1 = None
        hint_2 = None
        hint_3 = None
        for type_clue in DICT_HINTS_INFORMATION:
            # Check if the clue has not already been selected
            if not type_clue in self.clues:

                # Check if the clue has a value for the current country
                if not self.wikidata_code_country in DICT_HINTS_INFORMATION[type_clue]["exceptions"]:
                    dict_probabilities[type_clue] = DICT_HINTS_INFORMATION[type_clue]["probability"]

        if dict_probabilities != {}:
            # Sum all probabilities
            total = sum(dict_probabilities.values())

            for type_clue in dict_probabilities:
                dict_probabilities[type_clue] /= total

            hint_1 = self.select_clue(dict_probabilities)

            # Choose a second distinct clue
            if len(dict_probabilities) != 1:
                hint_2 = hint_1
                while hint_2 == hint_1:
                    hint_2 = self.select_clue(dict_probabilities)

                # Choose a third distinct clue
                if len(dict_probabilities) != 2:
                    hint_3 = hint_1
                    while hint_3 == hint_1 or hint_3 == hint_2:
                        hint_3 = self.select_clue(dict_probabilities)

        return hint_1, hint_2, hint_3

    def select_clue(self, dict_probabilities):
        """
        Select randomly a clue given the probabilities of the clues.

        Parameters
        ----------
        dict_probabilities : dict
            Dictionary of clues with their associated probability.

        Returns
        -------
        str
            Name of the randomly choosen clue.
        """
        probability = rd.random()
        sum_probabilities = 0
        for key in dict_probabilities:
            value_probability = dict_probabilities[key]
            if probability <= value_probability + sum_probabilities:
                return key
            sum_probabilities += value_probability

    def add_life(self):
        self.number_lives += 1
