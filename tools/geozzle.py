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
    ANDROID_MODE,
    IOS_MODE,
    REWARD_INTERSTITIAL,
    LIST_CLUES_EXCEPTIONS,
    DICT_WIKIDATA_LANGUAGE
)

from tools.sparql import (
    request_all_clues
)
from tools.kivyreview import (
    request_review
)
if ANDROID_MODE:
    from tools.kivads import (
        RewardedInterstitial
    )

if IOS_MODE:
    from pyobjus import autoclass # pylint: disable=import-error # type: ignore

#################
### Functions ###
#################

def insert_space_numbers(number: str, language: str) -> str:
    """
    Put spaces or comas each 3 numbers.
    
    Parameters
    ----------
    number : str
        String of a number
    language : str
        Code of the language
    
    Returns
    -------
    str
        New number formatted with delimitators.
    """
    if "." in number:
        list_int_decimals = number.split(".")
        if len(list_int_decimals[1]) >= 3:
            if len(list_int_decimals[0]) <= 3:
                list_int_decimals[1] = list_int_decimals[1][:2]
            else:
                list_int_decimals[1] = []
        number = ""
        for int_number in list_int_decimals[0]:
            number += int_number
        if list_int_decimals[1] != []:
            number += "."
        for dec_number in list_int_decimals[1]:
            number += dec_number

    if number[0] == "0" or len(number) <= 3:
        return number

    if language == "english":
        delimitation_character = ","
    else:
        delimitation_character = " "

    counter = 0
    list_characters = []
    new_number = ""
    for character in range(len(number)-1,-1,-1):
        value = number[character]
        if counter == 2:
            list_characters = [delimitation_character, value] + list_characters
            counter = 0
        else:
            list_characters.insert(0, value)
            counter += 1

    if list_characters[0] == delimitation_character:
        list_characters.pop(0)

    for character in list_characters:
        new_number += character
    return new_number

def format_clue(code_clue: str, value_clue: str, language: str) -> str:
    """
    Format the value of the clue to display something nice in the scrollview.
    
    Parameters
    ----------
    code_clue : str
        Code of the clue
    value_clue : str
        Value associated to the clue
    language : str
        Code of the language
    
    Returns
    -------
    str
        Value of the clue formatted.
    """
    has_changed_language = False
    if language != TEXT.language:
        has_changed_language = True
        original_language = TEXT.language
        TEXT.change_language(language=language)

    name_key = TEXT.clues[code_clue]

    # Capitalize some clues
    if code_clue in ["driving_side", "currency", "official_language"]:
        value_clue = value_clue.capitalize()

    # Take the mean of the GDP values
    if code_clue == "nominal_GDP":
        list_gdp = value_clue.split(", ")
        mean_gdp = 0
        for gdp in list_gdp:
            mean_gdp += int(gdp)
        mean_gdp /= len(list_gdp)
        if mean_gdp >= 1000000:
            value_clue = str(int(mean_gdp/1000000))
        else:
            value_clue = str(mean_gdp/1000000)

    # Add spaces between the numbers
    if code_clue in ["area", "population", "nominal_GDP", "median_income"]:
        value_clue = insert_space_numbers(value_clue, language)

    value_clue = "– " + name_key + " : " + value_clue

    # Add the units when needed
    if code_clue == "area":
        value_clue += " km²"
    if code_clue == "nominal_GDP":
        value_clue += " M$"
    if code_clue == "age_of_majority":
        value_clue += TEXT.clues["years"]
    if code_clue == "population":
        value_clue += TEXT.clues["inhabitants"]

    if has_changed_language:
        TEXT.change_language(language=original_language)

    return value_clue

def calculate_score_clues(part_highscore: float, nb_clues: int) -> int:
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
    # If the user guesses with less than 4 clues, he has all points
    if nb_clues <= 4:
        return int(part_highscore)

    # Lose points after, until using more than 14 clues
    part_highscore = part_highscore * (1 - (nb_clues-4)/10)

    # No negative score
    if part_highscore <= 0:
        return 0

    return int(part_highscore)


# Create the ad instance
if ANDROID_MODE:
    ad = RewardedInterstitial(REWARD_INTERSTITIAL, on_reward=None)
elif IOS_MODE:
    ad = autoclass("adInterstitial").alloc().init()
else:
    ad = None


def watch_ad(ad_callback):
    global ad
    if ANDROID_MODE:
        ad.on_reward = ad_callback
        ad.show()
        ad = RewardedInterstitial(REWARD_INTERSTITIAL, on_reward=None)
    elif IOS_MODE:
        ad.InterstitialView()
        ad_callback()
        # ad = autoclass("adInterstitial").alloc().init()
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
    dict_clues: dict
    # List of the at most three hints randomly choosen
    list_current_hints: list
    # The list of the wikidata code countries
    list_all_countries: list
    # The countries left to guess (wikidata code countries)
    list_countries_left: list
    # Dict of all clues (not only the one selected by the user)
    dict_all_clues: dict

    def create_new_game(self, continent: str = "Europe") -> bool:
        """
        Create a new game.

        Parameters
        ----------
        continent : str, optional (default is "Europe")
            Code name of the continent.

        Returns
        -------
        bool
            Whether the creation of the game has worked or not.
        """
        self.code_continent = continent
        has_success = self.load_data()
        return has_success

    def load_data(self) -> bool:
        """
        Load the data for a new game.
        It also load the data of the previous game is there was an ongoing one.
        It also create the request to get all clues of the current country.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            Whether the creation of the game has worked or not.
        """
        user_data_continent = USER_DATA.continents[self.code_continent]
        last_country = user_data_continent["current_country"]

        self.list_current_hints = last_country["list_current_hints"]
        self.dict_clues = last_country["dict_clues"]
        self.number_lives = user_data_continent["number_lives"]
        self.number_lives_used_game = last_country["number_lives_used_game"]

        self.list_all_countries = list(
            DICT_COUNTRIES[USER_DATA.language][self.code_continent].keys())
        self.list_countries_left = [
            country for country in self.list_all_countries if not country in user_data_continent["countries_unlocked"]]

        if last_country["country"] != "":
            self.wikidata_code_country = last_country["country"]
            self.dict_all_clues = last_country["dict_all_clues"]

        else:
            self.wikidata_code_country = rd.choice(self.list_countries_left)
            self.dict_all_clues = {}

            # Request all clues for the current country in French and English
            dict_all_clues_en = request_all_clues(
                wikidata_code_country=self.wikidata_code_country,
                code_continent=self.code_continent,
                language=DICT_WIKIDATA_LANGUAGE["english"])
            dict_all_clues_fr = request_all_clues(
                wikidata_code_country=self.wikidata_code_country,
                code_continent=self.code_continent,
                language=DICT_WIKIDATA_LANGUAGE["french"])

            if dict_all_clues_en is None or dict_all_clues_fr is None:
                return False
            
            self.dict_all_clues["french"] = dict_all_clues_fr
            self.dict_all_clues["english"] = dict_all_clues_en

            # Update the information is the USER_DATA
            USER_DATA.continents[self.code_continent][
                "current_country"]["country"] = self.wikidata_code_country
            USER_DATA.continents[self.code_continent][
                "current_country"]["dict_all_clues"] = self.dict_all_clues

            USER_DATA.save_changes()

        return True

    def add_clue(self, name_clue: str):
        """
        Add a clue in the dictionary of clues.

        Parameters
        ----------
        name_clue : str
            Name of the clue (depending on the language)

        Returns
        -------
        None
        """
        # Reset the list of hints
        self.list_current_hints = []
        USER_DATA.continents[self.code_continent][
            "current_country"]["list_current_hints"] = []

        # Get the code of the clue with its name
        for code_clue in TEXT.clues:
            if TEXT.clues[code_clue] == name_clue:
                break

        for language in ["french", "english"]:
            if not code_clue in ["ISO_3_code", "flag"]:
                value_clue = format_clue(
                    code_clue=code_clue,
                    value_clue=self.dict_all_clues[language][code_clue],
                    language=language)
            else:
                value_clue = self.dict_all_clues[language][code_clue]
            self.dict_clues[language][code_clue] = value_clue
            USER_DATA.continents[self.code_continent][
                "current_country"]["dict_clues"][language][code_clue] = value_clue

        USER_DATA.save_changes()

    def check_country(self, guessed_country: str) -> bool:
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

    def detect_game_over(self) -> bool:
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
            if not has_already_reached_30 and ANDROID_MODE:
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
        highscore += int((max(3 - self.number_lives_used_game, 0)
                         * half_part_highscore) / 3)

        # Depending on the number of clues used => the other half of the score
        highscore += calculate_score_clues(
            part_highscore=half_part_highscore,
            nb_clues=len(self.dict_clues[TEXT.language])
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

        # Load the preselected clues if there are some
        if self.list_current_hints != []:
            hint_1 = self.list_current_hints[0]
            if len(self.list_current_hints) >= 2:
                hint_2 = self.list_current_hints[1]
                if len(self.list_current_hints) >= 3:
                    hint_3 = self.list_current_hints[2]

            return hint_1, hint_2, hint_3

        # Choose three new clues
        for type_clue in self.dict_all_clues[TEXT.language]:
            # Check if the clue has not already been selected
            if not type_clue in self.dict_clues[TEXT.language] and not type_clue in LIST_CLUES_EXCEPTIONS:
                # Get the probability of the clue
                dict_probabilities[type_clue] = DICT_HINTS_INFORMATION[type_clue]

        if dict_probabilities != {}:
            # Sum all probabilities
            total = sum(dict_probabilities.values())

            for type_clue in dict_probabilities:
                dict_probabilities[type_clue] /= total

            hint_1 = self.select_clue(dict_probabilities)
            self.list_current_hints.append(hint_1)

            # Choose a second distinct clue
            if len(dict_probabilities) != 1:
                hint_2 = hint_1
                while hint_2 == hint_1:
                    hint_2 = self.select_clue(dict_probabilities)
                self.list_current_hints.append(hint_2)

                # Choose a third distinct clue
                if len(dict_probabilities) != 2:
                    hint_3 = hint_1
                    while hint_3 == hint_1 or hint_3 == hint_2:
                        hint_3 = self.select_clue(dict_probabilities)
                    self.list_current_hints.append(hint_3)

        USER_DATA.continents[self.code_continent][
            "current_country"]["list_current_hints"] = self.list_current_hints
        USER_DATA.save_changes()

        return hint_1, hint_2, hint_3

    def select_clue(self, dict_probabilities: dict) -> str:
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
