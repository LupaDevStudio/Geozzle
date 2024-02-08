"""
Module of the main backend of Geozzle.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd
import time
import copy

### Local imports ###

from tools.constants import (
    USER_DATA,
    MAX_HIGHSCORE,
    TEXT,
    DICT_COUNTRIES,
    DICT_HINTS_INFORMATION,
    CURRENT_COUNTRY_INIT,
    MOBILE_MODE,
    REWARD_INTERSTITIAL
)

from tools.sparql import (
    request_clues
)
from tools.kivyreview import (
    request_review
)
if MOBILE_MODE:
    from tools.kivads import (
        RewardedInterstitial
    )

#################
### Functions ###
#################


def calculate_score_clues(part_highscore: float, nb_clues: int):
    """
    Calculate the score of the user depending only on the number of clues used.
    
    Parameters
    ----------
    part_highscore : float
        Part of the score to attribute to the clues.
    nb_clues : int
        Number of clues used to guess the country.
    
    Returns
    -------
    int
        Score of the user for the clues part.
    """
    # If the user guesses with less than three clues, he has all points
    if nb_clues <= 4:
        return int(part_highscore)

    # Lose points after
    lost_points = part_highscore * (1 - nb_clues / 6)
    part_highscore -= lost_points

    if part_highscore <= 0:
        return 0

    return int(part_highscore)


# Create the ad instance
if MOBILE_MODE:
    ad = RewardedInterstitial(REWARD_INTERSTITIAL, on_reward=None)
else:
    ad = None


def watch_ad(ad_callback):
    global ad
    if MOBILE_MODE:
        ad.on_reward = ad_callback
        ad.show()
        ad = RewardedInterstitial(REWARD_INTERSTITIAL, on_reward=None)
    else:
        print("No ads to show outside mobile mode")
        ad_callback()

#############
### Class ###
#############


class Game():
    # Number of lives left for the continent
    number_lives: int
    # Number of lives used for this game
    number_lives_used_game: int
    code_continent: str
    wikidata_code_country: str
    clues: dict
    # The list of the wikidata code countries
    list_all_countries: list
    # The countries left to guess (wikidata code countries)
    list_countries_left: list

    def create_new_game(self, continent:str="Europe"):
        """
        Create a new game.
        
        Parameters
        ----------
        continent : str, optional (default is "Europe")
            Code name of the continent.
        
        Returns
        -------
        None
        """
        self.code_continent = continent
        self.load_data()

    def load_data(self):
        """
        Load the data for a new game.
        It also load the data of the previous game is there was an ongoing one.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        user_data_continent = USER_DATA.continents[self.code_continent]
        self.clues = user_data_continent["current_country"]["clues"]
        self.number_lives = user_data_continent["number_lives"]
        self.number_lives_used_game = user_data_continent["current_country"]["number_lives_used_game"]

        self.list_all_countries = list(
            DICT_COUNTRIES[USER_DATA.language][self.code_continent].keys())
        self.list_countries_left = [
            country for country in self.list_all_countries if not country in user_data_continent["countries_unlocked"]]

        last_country = user_data_continent["current_country"]["country"]
        if user_data_continent["current_country"]["country"] != "":
            self.wikidata_code_country = last_country
        else:
            self.wikidata_code_country = rd.choice(self.list_countries_left)
            USER_DATA.continents[self.code_continent]["current_country"]["country"] = self.wikidata_code_country
            USER_DATA.save_changes()

    def add_clue(self, name_clue: str):
        """
        Add a clue in the dictionary of clues.
        It also create the request for the associated clue.
        
        Parameters
        ----------
        name_clue : str
            Name of the clue (depending on the language)
        
        Returns
        -------
        str
            Value associated to the clue.
        """

        # Get the code of the clue with its name
        for code_clue in TEXT.clues:
            if TEXT.clues[code_clue] == name_clue:
                break

        value_clue = request_clues(
            code_clue, self.wikidata_code_country, self.code_continent)
        if value_clue is None:
            return
        self.clues[code_clue] = value_clue
        USER_DATA.continents[self.code_continent]["current_country"]["clues"][code_clue] = value_clue
        USER_DATA.save_changes()
        return value_clue

    def check_country(self, guessed_country: str):
        """
        Check if the country proposed by the user is the correct one.
        
        Parameters
        ----------
        guessed_country : str
            Name of the country proposed by the user.
        
        Returns
        -------
        bool
            Boolean according to which the country proposed by the user is correct or not.
        """
        # Find the wikidata code associated to the country
        for wikidata_code_country in DICT_COUNTRIES[USER_DATA.language][self.code_continent]:
            if DICT_COUNTRIES[USER_DATA.language][self.code_continent][wikidata_code_country] == guessed_country:
                break

        # Check if the user has found the correct country
        if self.wikidata_code_country == wikidata_code_country:
            USER_DATA.continents[self.code_continent]["countries_unlocked"].append(
                wikidata_code_country)
            USER_DATA.continents[self.code_continent]["current_country"] = copy.deepcopy(
                CURRENT_COUNTRY_INIT)
            USER_DATA.save_changes()
            self.list_countries_left.remove(wikidata_code_country)
            return True

        # Reduce the number of lives if the user has made a mistake
        self.number_lives -= 1
        self.number_lives_used_game += 1
        USER_DATA.continents[self.code_continent]["number_lives"] = self.number_lives
        USER_DATA.continents[self.code_continent]["current_country"][
            "number_lives_used_game"] = self.number_lives_used_game
        if USER_DATA.continents[self.code_continent]["lost_live_date"] is None:
            USER_DATA.continents[self.code_continent]["lost_live_date"] = time.time(
            )
        USER_DATA.save_changes()
        return False

    def detect_game_over(self):
        """
        Detect if this is the game over or not.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        bool
            Boolean according to which it is the game over or not.
        """
        # Reset the current dict of clues
        if self.number_lives <= 0:
            return True
        return False

    def reset_data_game_over(self):
        """
        When the user is in game over, the dict of clues is resetted.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        USER_DATA.continents[self.code_continent]["current_country"] = copy.deepcopy(
            CURRENT_COUNTRY_INIT)
        USER_DATA.save_changes()

    def update_percentage(self):
        """
        Update the percentage of completion of the continent.
        It is calculated based on the number of countries already guessed.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        # 100% of completion when the continent is over
        if self.list_countries_left == []:
            percentage = 100

        else:
            nb_all_countries = len(self.list_all_countries)
            nb_guessed_countries = len(
                USER_DATA.continents[self.code_continent]["countries_unlocked"])
            percentage = int(100 * (nb_guessed_countries / nb_all_countries))

        # Launch the review if the user reaches 30% for the first time
        if percentage > 30:
            has_already_reached_30 = False
            for continent_key in USER_DATA.continents:
                if USER_DATA.continents[continent_key]["percentage"] > 30:
                    has_already_reached_30 = True
            if not has_already_reached_30 and MOBILE_MODE:
                request_review()

        # Save the changes in the USER_DATA
        USER_DATA.continents[self.code_continent]["percentage"] = percentage
        USER_DATA.save_changes()

    def update_score(self):
        """
        Update the score of the user in its data when he has guessed a country.
        The score is divided into two parts:
            - the number of lives he used to guess the country
            - the number of clues he used to guess the country
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        highscore = USER_DATA.continents[self.code_continent]["highscore"]
        part_highscore = MAX_HIGHSCORE / len(self.list_all_countries)
        half_part_highscore = part_highscore / 2

        # Depending on the number of lives => half the score
        highscore += int((max(3-self.number_lives_used_game, 0) * half_part_highscore)/3)

        # Depending on the number of clues used => the other half of the score
        highscore += calculate_score_clues(
            part_highscore=half_part_highscore,
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
        """
        Add a life to the user after he watches an add.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.number_lives += 1
        USER_DATA.continents[self.code_continent]["number_lives"] += 1
        USER_DATA.save_changes()
