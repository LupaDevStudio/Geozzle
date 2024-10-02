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
import os
from typing import Literal, Callable

### Local imports ###

from tools.constants import (
    DICT_COUNTRIES,
    DICT_HINTS_INFORMATION,
    CURRENT_COUNTRY_INIT,
    REWARD_INTERSTITIAL,
    LIST_CLUES_EXCEPTIONS,
    DICT_WIKIDATA_LANGUAGE,
    NUMBER_CREDITS,
    DICT_CONTINENTS_PRIMARY_COLOR,
    PRICE_BACKGROUND,
    LIST_CONTINENTS,
    REWARD_AD
)
from tools.path import (
    PATH_BACKGROUNDS,
    ANDROID_MODE,
    IOS_MODE,
    PATH_LANGUAGE,
    PATH_USER_DATA
)
from tools.basic_tools import (
    load_json_file,
    save_json_file
)
from tools.sparql import (
    request_all_clues
)
from tools.kivyreview import (
    request_review
)
if ANDROID_MODE:
    from tools.kivads import (
        RewardedInterstitial,
        RewardedAd,
        TestID
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


def get_nb_stars(list_clues: list[str]) -> int:
    nb_stars = 3
    for code_clue in list_clues:
        if DICT_HINTS_INFORMATION[code_clue]["category"] < nb_stars:
            nb_stars = DICT_HINTS_INFORMATION[code_clue]["category"]
    return nb_stars

#############
### Class ###
#############

class AdContainer():

    nb_max_reload = 3

    def __init__(self) -> None:
        self.current_ad = None
        self.load_ad()
        print("Ad container initialization")

    def watch_ad(self, ad_callback: Callable, ad_fail: Callable = lambda: 1 + 1):
        reload_id = 0
        if ANDROID_MODE:
            self.current_ad: RewardedAd
            print("try to show ads")
            print("Ad state:", self.current_ad.is_loaded())

            # Reload ads if fail
            while not self.current_ad.is_loaded() and reload_id < self.nb_max_reload:
                self.current_ad = None
                self.load_ad()
                time.sleep(0.3)
                reload_id += 1
                print("Reload ad", reload_id)

            # Check if ads is finally loaded
            if not self.current_ad.is_loaded():
                ad_fail()
                self.current_ad = None
                self.load_ad()
            else:
                self.current_ad.on_reward = ad_callback
                self.current_ad.show()
        elif IOS_MODE:
            # self.current_ad.RewardedView()
            self.current_ad.InterstitialView()
            ad_callback()
        else:
            print("No ads to show outside mobile mode")
            ad_callback()

    def load_ad(self):
        print("try to load ad")
        if ANDROID_MODE:
            self.current_ad = RewardedAd(
                # REWARD_INTERSTITIAL,
                # TestID.REWARD,
                REWARD_AD,
                on_reward=None)
        elif IOS_MODE:
            # self.current_ad = autoclass("adRewarded").alloc().init()
            self.current_ad = autoclass("adInterstitial").alloc().init()
        else:
            self.current_ad = None


AD_CONTAINER = AdContainer()

############
### Game ###
############


class Game():
    # Number of lives left for this game
    number_lives: int

    # Number of credits left to use
    number_credits: int

    # List of the continents
    list_continents: list[str]

    # List of countries to guess (wikidata codes)
    list_countries_to_guess: list[str]

    # Dict of countries encountered during the game
    # {"code_country": {"list_clues": ["clue_1" ,"clue_2"], "multiplier": 1.2, "guessed": True, "nb_lives_used":0}}
    dict_guessed_countries: dict

    # List of the codes of the current clues
    list_current_clues: list[str]

    # Dict of the results of the request for the current country
    # {"english": {"capital": "London", ...}, "french": {"capital": "Londres", ...}}
    dict_details_country: dict

    # Index of the current country in the list of countries to guess successively
    current_country_index: int

    # List of the wikidata codes of the all the other countries in the spinner
    # ["code_country_1", "code_country_2", ...].}
    list_countries_in_spinner: list[str]

    @ property
    def has_lives(self) -> bool:
        return self.number_lives > 0

    @ property
    def can_watch_ad(self) -> bool:
        return self.number_credits > 0

    @ property
    def current_guess_country(self) -> str:
        """Wikidata code of the country to guess currently"""
        return self.list_countries_to_guess[self.current_country_index]

    @ property
    def current_guess_continent(self) -> str:
        """Code of the current continent"""
        return self.list_continents[self.current_country_index]

    @ property
    def data_already_loaded(self) -> bool:
        """If the data of the current country has already been downloaded from wikidata."""
        if self.dict_details_country == {}:
            return False
        return TEXT.language in self.dict_details_country

    @property
    def current_multiplier(self):
        # Count the streak i.e. the number of countries guessed without mistakes
        streak = 0
        for i in range(self.current_country_index):
            country_code = self.list_countries_to_guess[i]
            nb_lives_used = self.dict_guessed_countries[country_code]["nb_lives_used"]
            if nb_lives_used == 0:
                streak += 1
            else:
                streak = 0

        # Compute the multiplier
        multiplier = 1. + 0.2 * streak

        return multiplier

    def __init__(self, dict_to_load: dict) -> None:
        self.number_lives = dict_to_load.get("number_lives", 3)
        self.number_credits = dict_to_load.get(
            "number_credits", NUMBER_CREDITS)
        self.current_country_index = dict_to_load.get(
            "current_country_index", 0)

        self.list_continents = dict_to_load.get(
            "list_continents", [])
        self.list_countries_to_guess = dict_to_load.get(
            "list_countries_to_guess", [])
        self.list_current_clues = dict_to_load.get(
            "list_current_clues", [])

        self.dict_guessed_countries = dict_to_load.get(
            "dict_guessed_countries", {})
        self.dict_details_country = dict_to_load.get(
            "dict_details_country", {})
        self.list_countries_in_spinner = dict_to_load.get(
            "list_countries_in_spinner", {})

    def build_list_continents(self):
        self.list_continents = LIST_CONTINENTS.copy()
        rd.shuffle(self.list_continents)

    def get_random_country(self, code_continent: str, nb_for_random_choice: int = 3):
        """
        Select a random country of the given continent.

        Parameters
        ----------
        code_continent : str
            Continent code.
        nb_for_random_choice : int, optional (default is 3)
            Number of countries to select among the least played for the random choice.

        Returns
        -------
        str
            Code of the country.
        """

        # Get the list of countries
        countries_list = list(DICT_COUNTRIES["english"][code_continent].keys())

        # Get the number of times each country has been played
        nb_times_played_list = []
        for country in countries_list:
            if country in USER_DATA.stats[code_continent]:
                nb_times_played_list.append(
                    USER_DATA.stats[code_continent][country]["nb_times_played"])
            else:
                nb_times_played_list.append(0)

        # Sort the indices of the list
        index_order = [i[0]
                       for i in sorted(enumerate(nb_times_played_list), key=lambda x: x[1])]

        # Extract the countries for the random choice
        countries_for_random_choice = []
        for i in range(nb_for_random_choice):
            countries_for_random_choice.append(countries_list[index_order[i]])

        # Pick a random country
        country_index = rd.randrange(nb_for_random_choice)

        return countries_for_random_choice[country_index]

    def get_other_countries_for_spinner_list(self, code_continent: str, current_country, nb_side_countries=11):
        # Get the list of countries in the continent
        countries_list: list = DICT_COUNTRIES["english"][code_continent].copy()

        # Exclude the current_country
        countries_list.remove(current_country)

        # Shuffle the list
        rd.shuffle(countries_list)

        # Select a sample
        other_countries_for_spinner_list = countries_list[:nb_side_countries]

        return other_countries_for_spinner_list

    def build_list_countries(self):
        self.list_countries_to_guess = []

        # Iterate over the continents to choose one country for each
        for code_continent in self.list_continents:
            country = self.get_random_country(code_continent)
            self.list_countries_to_guess.append(country)

    def build_list_countries_in_spinner(self):
        self.list_countries_in_spinner = self.get_other_countries_for_spinner_list(
            self.current_guess_continent, self.current_guess_country)

    def build_dict_details_country(self):
        # Reload only if no data available in the language
        if USER_DATA.language not in self.dict_details_country:
            self.dict_details_country[USER_DATA.language] = request_all_clues(
                wikidata_code_country=self.current_guess_country,
                code_continent=self.current_guess_continent, wikidata_language=DICT_WIKIDATA_LANGUAGE[USER_DATA.language])

            if self.dict_details_country[USER_DATA.language] is None:
                return False

            # Find alternative language
            if USER_DATA.language == "french":
                alternative_language = "english"
            else:
                alternative_language = "french"

            # Deal with cases when user request in a language and change and not the same clues in both languages
            for code_clue in self.dict_guessed_countries[self.current_guess_country]["list_clues"]:
                if code_clue not in self.dict_details_country[USER_DATA.language]:
                    self.dict_details_country[USER_DATA.language][code_clue] = self.dict_details_country[alternative_language][code_clue]

        return True

    def build_dict_guessed_countries(self):
        self.dict_guessed_countries = {
            country_code: {
                "list_clues": [],
                "multiplier": 1,
                "guessed": False,
                "nb_lives_used": 0} for country_code in self.list_countries_to_guess
        }

    def launch_game(self) -> bool:
        if self.list_continents == []:
            self.build_list_continents()
        if self.list_countries_to_guess == []:
            self.build_list_countries()
        if self.dict_guessed_countries == {}:
            self.build_dict_guessed_countries()
        if self.list_countries_in_spinner == []:
            self.build_list_countries_in_spinner()
        request_status = self.build_dict_details_country()

        if not request_status:
            return False

        if self.list_current_clues == []:
            self.choose_clues()
        USER_DATA.save_changes()

        return True

    def choose_clues(self):
        """
        Choose the four clues that will be proposed to the player.
        If possible, the three categories should be available.
        """

        # Extract the list of clues that have already been used
        clues_already_used = self.dict_guessed_countries[self.current_guess_country]["list_clues"]

        # Create the list of all 1 star, 2 stars and 3 stars clues avoiding the ones that have already been used
        clues_by_categories = {1: [], 2: [], 3: []}
        for clue in DICT_HINTS_INFORMATION:
            current_category = DICT_HINTS_INFORMATION[clue]["category"]
            if clue not in clues_already_used and clue in self.dict_details_country[USER_DATA.language]:
                clues_by_categories[current_category].append(clue)

        # Count the number of clues for each category
        nb_clues_per_category = {
            1: len(clues_by_categories[1]),
            2: len(clues_by_categories[2]),
            3: len(clues_by_categories[3])
        }
        remaining_clues = []

        # Add the clues for each category
        list_current_clues = []
        for i in range(1, 4):
            if nb_clues_per_category[i] > 0:
                clue_index = rd.randrange(nb_clues_per_category[i])
                list_current_clues.append(clues_by_categories[i][clue_index])
                for j in range(nb_clues_per_category[i]):
                    if j == clue_index:
                        continue
                    remaining_clues.append(clues_by_categories[i][j])

        # Add additional random clues
        shuffled_indices = list(range(len(remaining_clues)))
        rd.shuffle(shuffled_indices)
        additional_clues_indices = shuffled_indices[:min(
            len(remaining_clues), 4 - len(list_current_clues))]
        for i in range(len(additional_clues_indices)):
            list_current_clues.append(
                remaining_clues[additional_clues_indices[i]])

        # Update the list
        self.list_current_clues = list_current_clues.copy()

        # Fill the list with None values
        while len(self.list_current_clues) < 4:
            self.list_current_clues.append(None)

    def ask_clue(self, code_clue: str):
        # Add the new clue in the list of clues used
        self.dict_guessed_countries[self.current_guess_country][
            "list_clues"].append(code_clue)

        # Reset the list of clues
        self.list_current_clues = []
        self.choose_clues()

        # Save the changes
        USER_DATA.save_changes()

    def watch_ad(self):
        self.number_lives += 1
        self.number_credits -= 1
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
        # TODO Paul (peut-être se resservir de la fonction qui avait déjà été codée avant)
        pass

    def go_to_next_country(self):
        self.dict_guessed_countries[self.current_guess_country]["guessed"] = True
        previous_multiplier = self.dict_guessed_countries[self.current_guess_country]["multiplier"]

        # Update the index of the current country
        self.current_country_index += 1

        # Check the end of the game or not
        if self.current_country_index >= 6:
            self.end_game()
        else:
            # Update the multiplier
            self.dict_guessed_countries[self.current_guess_country]["multiplier"] = self.current_multiplier

            # Rebuild the dict of details of the next country
            self.dict_details_country = {}
            # TODO faire quelque chose avec request status
            request_status = self.build_dict_details_country()

            # Rebuild the list of current clues
            self.list_current_clues = []

            # Rebuild the list of countries in spinner
            self.list_countries_in_spinner = []
            self.build_list_countries_in_spinner()

    def end_game(self):
        """
        End the current game and reset the class.
        """

        score = self.compute_final_game_score()
        USER_DATA.update_points_and_score(score=score)
        USER_DATA.update_stats(
            dict_guessed_countries=self.dict_guessed_countries,
            list_continents=self.list_continents)

        # Reset all variables in the game when it's over
        self.number_lives = 3
        self.number_credits = NUMBER_CREDITS
        self.current_country_index = 0
        self.list_continents = []
        self.list_countries_to_guess = []
        self.list_current_clues = []
        self.dict_guessed_countries = {}
        self.dict_details_country = {}
        self.list_countries_in_spinner = {}

    def compute_final_game_score(self) -> int:
        # TODO Paul calculer le score avec ta fonction et le retourner
        pass

    def export_as_dict(self) -> dict:
        return {
            "number_lives": self.number_lives,
            "number_credits": self.number_credits,
            "list_continents": self.list_continents,
            "list_countries_to_guess": self.list_countries_to_guess,
            "dict_guessed_countries": self.dict_guessed_countries,
            "list_current_clues": self.list_current_clues,
            "dict_details_country": self.dict_details_country,
            "current_country_index": self.current_country_index,
            "list_countries_in_spinner": self.list_countries_in_spinner
        }


class OldGame():
    # Number of lives left for the continent
    number_lives: int
    # Number of lives used for this game
    number_lives_used_game: int
    code_continent: str
    wikidata_code_country: str
    dict_clues: dict
    # List of the at most three hints randomly chosen
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

    def is_already_loaded(self) -> bool:
        """
        Indicate if the game is already loaded or not.

        Returns
        -------
        bool
            _description_
        """
        user_data_continent = USER_DATA.continents[self.code_continent]
        last_country = user_data_continent["current_country"]
        if last_country["country"] != "":
            if TEXT.language not in last_country["dict_all_clues"]:
                return False
            else:
                return True
        else:
            return False

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
            wikidata_language=DICT_WIKIDATA_LANGUAGE[TEXT.language])

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
        When the user is in game over, the dict of clues is reset.

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
                dict_probabilities[type_clue] = DICT_HINTS_INFORMATION[type_clue]["probability"]

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
            Name of the randomly chosen clue.
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

#################
### User data ###
#################


class UserData():
    """
    A class to store the user data.
    """

    @property
    def can_buy_background(self):
        return self.points >= PRICE_BACKGROUND

    def __init__(self) -> None:
        data = load_json_file(PATH_USER_DATA)
        self.game: Game = Game(data.get("game", {}))
        self.language: Literal["english", "french"] = data.get(
            "language", "english")
        self.sound_volume: float = data.get("sound_volume", 0.5)
        self.music_volume: float = data.get("music_volume", 0.5)
        self.highscore: int = data.get("highscore", 0)
        self.points: int = data.get("points", 0)
        self.stats: int = data.get(
            "stats",
            {
                "Europe": {},
                "Asia": {},
                "Africa": {},
                "North_America": {},
                "South_America": {},
                "Oceania": {},
            })
        self.unlocked_backgrounds: list[str] = data.get(
            "unlocked_backgrounds", [])
        if self.unlocked_backgrounds == []:
            self.init_backgrounds()
        self.save_changes()

    def init_backgrounds(self):
        """
        Give a background for each continent when the user starts playing for the first time.
        """

        for code_continent in list(DICT_CONTINENTS_PRIMARY_COLOR.keys()):
            code_background = rd.choice(os.listdir(
                PATH_BACKGROUNDS + code_continent))
            self.unlocked_backgrounds.append(code_background)

    def get_nb_countries_with_stars(self, continent: str, target_nb_stars: int):
        """
        Compute the number of countries for a given continent with the target number of stars.

        Parameters
        ----------
        continent : str
            Continent code.
        target_nb_stars : int
            Number of stars to target.

        Returns
        -------
        int
            Number of countries
        """

        nb_countries = 0
        for country in self.stats[continent]:
            nb_stars = self.stats[continent][country]["nb_stars"]
            if nb_stars == target_nb_stars:
                nb_countries += 1

        return nb_countries

    def get_nb_countries(self, continent: str):
        """
        Compute the number of countries in a given continent.

        Parameters
        ----------
        continent : str
            Continent code.

        Returns
        -------
        int
            Number of countries
        """

        return len(DICT_COUNTRIES["english"][continent])

    def get_nb_stars_on_continent(self, continent: str):
        """
        Return the number of stars obtained on a given continent.

        Parameters
        ----------
        continent : str
            Continent code.

        Returns
        -------
        int
            Number of stars obtained on the continent.
        """

        nb_stars_on_continent = 0
        for country in self.stats[continent]:
            nb_stars = self.stats[continent][country]["nb_stars"]
            nb_stars_on_continent += nb_stars

        return nb_stars_on_continent

    def get_continent_progress(self, continent: str):
        """
        Return the progress of the continent in percent.
        This number corresponds to the number of stars obtained divided by the total number of stars.

        Parameters
        ----------
        continent : str
            Continent code.

        Returns
        -------
        int
            Percentage of progress.
        """

        # Extract the data
        nb_stars_on_continent = self.get_nb_stars_on_continent(continent)
        nb_countries_on_continent = self.get_nb_countries(continent)

        # Compute the percentage
        percentage = int(nb_stars_on_continent /
                         (3 * nb_countries_on_continent))

        return percentage

    def update_points_and_score(self, score: int):
        # Update the number of points
        self.points += score

        # Update the highscore if needed
        if score > self.highscore:
            self.highscore = score

        # Save the changes
        self.save_changes()

    def update_stats(self, dict_guessed_countries: dict, list_continents: list[str]):
        counter = 0
        for code_country in dict_guessed_countries:
            dict_details = dict_guessed_countries[code_country]
            if dict_details["guessed"]:
                code_continent = list_continents[counter]
                if not code_country in self.stats[code_continent]:
                    self.stats[code_continent][code_country] = {
                        "nb_times_played": 0,
                        "nb_stars": 1
                    }
                self.stats[code_continent][code_country]["nb_times_played"] += 1
                number_stars = get_nb_stars(
                    list_clues=dict_details["list_clues"])
                if number_stars > self.stats[code_continent][code_country]["nb_stars"]:
                    self.stats[code_continent][code_country]["nb_stars"] = number_stars
            else:
                break
            counter += 1

    def buy_new_background(self) -> dict:
        dict_return = {}

        # Reduce the number of points
        self.points -= PRICE_BACKGROUND

        # Choose randomly the continent and the background
        code_continent = rd.choice(list(DICT_CONTINENTS_PRIMARY_COLOR.keys()))
        code_background = rd.choice(os.listdir(
            PATH_BACKGROUNDS + code_continent))

        # If the background bought is new
        if code_background not in self.unlocked_backgrounds:
            self.unlocked_backgrounds.append(code_background)
            dict_return["is_new"] = True
        else:
            dict_return["is_new"] = False

        # Add the background in the shared data
        full_path = SHARED_DATA.add_new_background(
            code_background=code_background,
            code_continent=code_continent)

        # Save the changes
        self.save_changes()

        dict_return["code_continent"] = code_continent
        dict_return["full_path"] = full_path

        return dict_return

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
        data["game"] = self.game.export_as_dict()
        data["stats"] = self.stats
        data["points"] = self.points
        data["highscore"] = self.highscore
        data["music_volume"] = self.music_volume
        data["sound_volume"] = self.sound_volume
        data["unlocked_backgrounds"] = self.unlocked_backgrounds

        # Save this dictionary
        save_json_file(
            file_path=PATH_USER_DATA,
            dict_to_save=data)


USER_DATA = UserData()

############
### Text ###
############


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
        self.titles = data["titles"]
        self.home = data["home"]
        self.settings = data["settings"]
        self.gallery = data["gallery"]
        self.stats = data["stats"]
        self.game_question = data["game_question"]
        self.game_summary = data["game_summary"]
        self.game_over = data["game_over"]
        self.clues = data["clues"]
        self.tutorial = data["tutorial"]
        self.popup = data["popup"]


TEXT = Text(language=USER_DATA.language)


###################
### Backgrounds ###
###################

class SharedData():
    list_unlocked_backgrounds: list[str]  # list of the path of the images

    def __init__(self) -> None:
        self.list_unlocked_backgrounds = []
        for code_continent in list(DICT_CONTINENTS_PRIMARY_COLOR.keys()):
            for code_background in os.listdir(PATH_BACKGROUNDS + code_continent):
                if code_background in USER_DATA.unlocked_backgrounds:
                    self.add_new_background(
                        code_background=code_background,
                        code_continent=code_continent)

    def choose_random_background_continent(self, code_continent: str):
        list_corresponding_backgrounds = []
        for full_path in self.list_unlocked_backgrounds:
            if code_continent in full_path:
                list_corresponding_backgrounds.append(full_path)
        return rd.choice(list_corresponding_backgrounds)

    def add_new_background(self, code_background: str, code_continent: str) -> str:
        full_path = PATH_BACKGROUNDS + code_continent + "/" + code_background
        if full_path not in self.list_unlocked_backgrounds:
            self.list_unlocked_backgrounds.append(full_path)
        return full_path


SHARED_DATA = SharedData()
