"""
Module of the main backend of Geozzle.
"""

import random as rd

from tools.constants import (
    USER_DATA,
    MAX_HIGHSCORE
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
    continent: str
    country: str
    clues: dict
    list_all_countries: list
    list_countries_left: list # the countries left to guess

    def __init__(self, continent="Europe") -> None:
        self.continent = continent
        self.load_data()

    def load_data(self):
        user_data_continent = USER_DATA.continents[self.continent]
        self.clues = user_data_continent["current_country"]["clues"]
        self.number_lives = user_data_continent["current_country"]["nb_lives"]
        self.number_ads = user_data_continent["current_country"]["nb_ads"]

        # TODO mettre la bonne liste de pays avec les requêtes Wikidata (tous les pays d'un continent)
        self.list_all_countries = ["France", "England"]
        self.list_countries_left = [country for country in self.list_all_countries if not country in user_data_continent["countries_unlocked"]]

        last_country = user_data_continent["current_country"]["country"]
        if user_data_continent["current_country"]["country"] != "":
            self.country = last_country
        else:
            self.country = rd.choice(self.list_countries_left)

    def add_clue(self, type_clue):
        # TODO il faut ajouter au dictionnaire des indices avec la valeur associée, tout en faisant une requête Wikidata pour avoir la valeur associée (grâce au champ pays)
        self.clues[type_clue] = "1 m²"

    def check_country(self, guessed_country:str):
        if self.country == guessed_country:
            return True
        
        # Reduce the number of lives if the user has made a mistake
        self.number_lives -= 1
        return False

    def check_game_over(self):
        if self.number_lives <= 0:
            return True
        return False

    def update_percentage(self):
        percentage = USER_DATA.continents[self.continent]["percentage"]
        percentage += 1/len(self.list_all_countries)

        # Save the changes in the USER_DATA
        USER_DATA.continents[self.continent]["percentage"] = percentage
        USER_DATA.save_changes()

    def update_highscore(self):
        highscore = USER_DATA.continents[self.continent]["highscore"]
        part_highscore = MAX_HIGHSCORE / len(self.list_all_countries)

        # Depending on the number of lives => half the score
        highscore += (self.number_lives*part_highscore)/(2*3)

        # Depending on the number of clues used => the other half of the score
        highscore += calculate_highscore_clues(
            part_highscore=part_highscore/2,
            nb_clues=len(self.clues)
        )
        
        # Save the changes in the USER_DATA
        USER_DATA.continents[self.continent]["highscore"] = highscore
        USER_DATA.save_changes()
