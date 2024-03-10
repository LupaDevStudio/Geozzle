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
    from pyobjus import autoclass  # pylint: disable=import-error # type: ignore

#################
### Functions ###
#################


def insert_space_numbers(str_number: str, language: str) -> str:
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
    # Treat number with decimals
    if "." in str_number:
        list_int_decimals = str_number.split(".")
        int_part = list_int_decimals[0]
        decimal_part = list_int_decimals[1]

        # Crop the decimal part when too long
        if len(decimal_part) >= 3:
            if len(int_part) <= 3:
                decimal_part = decimal_part[:2]
            else:
                decimal_part = ""
        if len(int_part) >= 3:
            decimal_part = ""

        # Reconstruct the number with the integer and decimal parts
        str_number = int_part
        if decimal_part != "":
            str_number += "."
            str_number += decimal_part

    # Do not put separators for small numbers
    if "." in str_number or len(str_number) <= 3:
        return str_number

    # Choose between "," or " " for the delimitation character
    if language == "english":
        delimitation_character = ","
    else:
        delimitation_character = " "

    # Put the delimitator character each three numbers
    counter = 0
    list_characters = []
    new_str_number = ""
    for counter_character in range(len(str_number) - 1, -1, -1):
        value = str_number[counter_character]
        if counter == 2:
            list_characters = [delimitation_character, value] + list_characters
            counter = 0
        else:
            list_characters.insert(0, value)
            counter += 1

    if list_characters[0] == delimitation_character:
        list_characters.pop(0)

    for counter_character in list_characters:
        new_str_number += counter_character
    return new_str_number


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

    name_key = TEXT.clues[code_clue]

    # Delete odd characters
    try:
        value_clue = value_clue.replace("ʻ", "'")
        value_clue = value_clue.replace("ə", "e")
        list_odd_characters = []
        for counter_character in range(len(value_clue)):
            character = value_clue[counter_character]
            if ord(character) >= 550:
                list_odd_characters.append(character)
        for character in list_odd_characters:
            value_clue = value_clue.replace(character, "")
    except:
        pass

    # Capitalize some clues
    if code_clue in ["driving_side", "currency", "official_language"]:
        if ", " in value_clue:
            list_clues = value_clue.split(", ")
            value_clue = ""
            for clue in list_clues:
                value_clue += clue.capitalize() + ", "
            value_clue = value_clue[:-2]
        else:
            value_clue = value_clue.capitalize()

    # Separate the unit from the value
    unit = ""
    if code_clue == "area":
        list_separated = value_clue.split(" ")
        value_clue = list_separated[0]
        unit = list_separated[1]

    # Take the mean of the GDP values
    try:
        if code_clue == "nominal_GDP":
            list_gdp = value_clue.split(", ")

            for counter_gdp_unit in range(len(list_gdp)):
                list_separated = list_gdp[counter_gdp_unit].split(" ")
                value = list_separated[0]
                unit = list_separated[1]
                list_gdp[counter_gdp_unit] = value

            mean_gdp = 0
            for gdp in list_gdp:
                if not "." in gdp:
                    mean_gdp += int(gdp)
                else:
                    mean_gdp += int(float(gdp))
            mean_gdp /= len(list_gdp)
            billion = 1000000000
            if mean_gdp >= billion:
                value_clue = str(int(mean_gdp / billion))
            else:
                value_clue = str(mean_gdp / billion)
    except:
        pass

    try:
        if code_clue == "population":
            list_pop = value_clue.split(", ")
            list_pop_int = []
            for element in list_pop:
                list_pop_int.append(int(element))
            value_clue = str(max(list_pop_int))
    except:
        pass

    # Add spaces between the numbers
    try:
        if code_clue in ["area", "population", "nominal_GDP"]:
            value_clue = insert_space_numbers(value_clue, language)
    except:
        pass

    # Some clean
    try:
        if value_clue[0: 3] == "., ":
            value_clue = value_clue.replace("., ", "")
        if value_clue[-3:] == ", .":
            value_clue = value_clue.replace(", .", "")
    except:
        pass

    value_clue = "– " + name_key + " : " + value_clue

    # Add the units when needed
    if code_clue == "area":
        value_clue += " " + unit
    if code_clue == "nominal_GDP":
        value_clue += TEXT.clues["billion"] + unit
    if code_clue == "age_of_majority":
        value_clue += TEXT.clues["years"]
    if code_clue == "population":
        value_clue += TEXT.clues["inhabitants"]

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
    # If the user guesses with less than 3 clues, he has all points
    if nb_clues <= 3:
        return part_highscore

    # Lose points after, until using more than 12 clues
    part_highscore = part_highscore * (1 - (nb_clues - 3) / 9)

    # No negative score
    if part_highscore <= 0:
        return 0

    return part_highscore


# # Create the ad instance
# if ANDROID_MODE:
#     ad = RewardedInterstitial(REWARD_INTERSTITIAL, on_reward=None)
# elif IOS_MODE:
#     ad = autoclass("adInterstitial").alloc().init()
# else:
#     ad = None


# def load_ad():
#     global ad
#     if ANDROID_MODE:
#         ad = RewardedInterstitial(REWARD_INTERSTITIAL, on_reward=None)
#     elif IOS_MODE:
#         ad = autoclass("adInterstitial").alloc().init()
#     else:
#         ad = None


# def watch_ad(ad_callback, ad_fail=lambda: 1 + 1):
#     global ad
#     if ANDROID_MODE:
#         print("try to show ads")
#         print("Ad is loaded", ad.is_loaded())
#         if not ad.is_loaded():
#             ad_fail()
#             ad = None
#             load_ad()
#         else:
#             ad.on_reward = ad_callback
#             ad.show()
#     elif IOS_MODE:
#         ad.InterstitialView()
#         ad_callback()
#     else:
#         print("No ads to show outside mobile mode")
#         ad_callback()

#############
### Class ###
#############


class AdContainer():
    def __init__(self) -> None:
        self.ads_list = []
        self.load_ad()
        print("Ad container initialization")

    def watch_ad(self, ad_callback, ad_fail=lambda: 1 + 1):
        current_ad = self.ads_list[-1]
        if ANDROID_MODE:
            current_ad: RewardedInterstitial
            print("try to show ads")
            print("Ad is loaded", current_ad.is_loaded())
            if not current_ad.is_loaded():
                ad_fail()
                current_ad = None
                self.load_ad()
            else:
                current_ad.on_reward = ad_callback
                current_ad.show()
        elif IOS_MODE:
            current_ad.InterstitialView()
            ad_callback()
        else:
            print("No ads to show outside mobile mode")
            ad_callback()

    def load_ad(self):
        print("try to load ad")
        if ANDROID_MODE:
            self.ads_list.append(RewardedInterstitial(
                REWARD_INTERSTITIAL, on_reward=None))
        elif IOS_MODE:
            self.ads_list.append(autoclass("adInterstitial").alloc().init())
        else:
            self.ads_list.append(None)


AD_CONTAINER = AdContainer()


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

    def create_new_game(self, code_continent: str = "Europe") -> bool:
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
        self.code_continent = code_continent
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
        self.number_lives = user_data_continent["number_lives"]
        self.number_lives_used_game = last_country["number_lives_used_game"]
        self.dict_clues = last_country["dict_clues"]

        self.list_all_countries = list(
            DICT_COUNTRIES[USER_DATA.language][self.code_continent].keys())
        self.list_countries_left = [
            country for country in self.list_all_countries if not country in user_data_continent["countries_unlocked"]]

        if last_country["country"] != "":
            self.wikidata_code_country = last_country["country"]
            self.dict_all_clues = last_country["dict_all_clues"]

            # If the user has changed the language, load the clues in the new language
            if TEXT.language not in self.dict_all_clues:
                has_success = self.load_dict_all_clues()
                if not has_success:
                    return False
                self.dict_clues[TEXT.language] = {}
            self.fill_dict_clues()

        else:
            self.wikidata_code_country = rd.choice(self.list_countries_left)
            self.dict_all_clues = {}

            # Request all clues for the current country in French and English
            has_success = self.load_dict_all_clues()
            if not has_success:
                return False

            # Update the information in the USER_DATA
            USER_DATA.continents[self.code_continent][
                "current_country"]["country"] = self.wikidata_code_country
            USER_DATA.save_changes()
        return True

    def load_dict_all_clues(self) -> bool:
        """
        Load the dict of all clues with requests to Wikidata, in the current language.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            Boolean indicating if the request has successed or not.
        """
        # Get all clues with the sparql request
        dict_all_clues_current_language = request_all_clues(
            wikidata_code_country=self.wikidata_code_country,
            code_continent=self.code_continent,
            language=DICT_WIKIDATA_LANGUAGE[TEXT.language])

        if dict_all_clues_current_language is None:
            return False

        self.dict_all_clues[TEXT.language] = dict_all_clues_current_language

        # Update the user data
        USER_DATA.continents[self.code_continent][
            "current_country"]["dict_all_clues"] = self.dict_all_clues
        USER_DATA.save_changes()

        return True

    def fill_dict_clues(self):
        """
        Fill the dict of clues of the current language, depending of the one of the other language.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Detect the reference language
        if TEXT.language == "english":
            ref_language = "french"
        else:
            ref_language = "english"

        if len(self.dict_clues[ref_language]) > len(self.dict_clues[TEXT.language]):

            # Add all clues of the reference dict of clues in the other one
            for code_clue in self.dict_clues[ref_language]:
                # Check if the clue exists in the results of the query
                if code_clue in self.dict_all_clues[TEXT.language]:
                    self.add_clue(code_clue=code_clue)

    def select_clue(self, name_clue: str):
        """
        Select the code name of the value and add it into the dictionary.

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

        self.add_clue(code_clue=code_clue)

    def add_clue(self, code_clue: str):
        """
        Add a clue in the dictionary of clues corresponding to the language.

        Parameters
        ----------
        name_clue : str
            Name of the clue (depending on the language)

        Returns
        -------
        None
        """

        if not code_clue in ["ISO_3_code", "flag"]:
            try:
                value_clue = format_clue(
                    code_clue=code_clue,
                    value_clue=self.dict_all_clues[TEXT.language][code_clue],
                    language=TEXT.language)
            except:
                print("Error in formatting")
                value_clue = self.dict_all_clues[TEXT.language][code_clue]
        else:
            value_clue = self.dict_all_clues[TEXT.language][code_clue]
        self.dict_clues[TEXT.language][code_clue] = value_clue

        USER_DATA.continents[self.code_continent][
            "current_country"]["dict_clues"][TEXT.language][code_clue] = value_clue
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

    def update_score(self) -> int:
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
        int
            Current score
        """
        current_score = 0
        highscore = USER_DATA.continents[self.code_continent]["highscore"]
        part_highscore = MAX_HIGHSCORE / len(self.list_all_countries)
        half_part_highscore = part_highscore / 2

        # Depending on the number of lives => half the score
        current_score += (max(3 - self.number_lives_used_game, 0)
                          * half_part_highscore) / 3

        # Depending on the number of clues used => the other half of the score
        current_score += calculate_score_clues(
            part_highscore=half_part_highscore,
            nb_clues=len(self.dict_clues[TEXT.language])
        )

        # Set the max score to 10 000
        new_score = min(10000, highscore + current_score)

        # Save the changes in the USER_DATA
        USER_DATA.continents[self.code_continent]["highscore"] = new_score
        USER_DATA.save_changes()

        return current_score

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

            hint_1 = self.choose_clue(dict_probabilities)
            self.list_current_hints.append(hint_1)

            # Choose a second distinct clue
            if len(dict_probabilities) != 1:
                hint_2 = hint_1
                while hint_2 == hint_1:
                    hint_2 = self.choose_clue(dict_probabilities)
                self.list_current_hints.append(hint_2)

                # Choose a third distinct clue
                if len(dict_probabilities) != 2:
                    hint_3 = hint_1
                    while hint_3 == hint_1 or hint_3 == hint_2:
                        hint_3 = self.choose_clue(dict_probabilities)
                    self.list_current_hints.append(hint_3)

        USER_DATA.continents[self.code_continent][
            "current_country"]["list_current_hints"] = self.list_current_hints
        USER_DATA.save_changes()

        return hint_1, hint_2, hint_3

    def choose_clue(self, dict_probabilities: dict) -> str:
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
        if self.number_lives == 3:
            USER_DATA.continents[self.code_continent]["lost_live_date"] = None
        USER_DATA.save_changes()
