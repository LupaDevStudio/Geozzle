###############
### Imports ###
###############

### Python imports ###

import requests
import sys
sys.path.append("../")
sys.path.append("./")
from typing import Literal

### Local imports ###

from tools.basic_tools.json import (
    save_json_file
)

from tools.constants import (
    DICT_WIKIDATA_CONTINENTS,
    DICT_WIKIDATA_LANGUAGE,
    URL_WIKIDATA,
    USER_DATA
)

from tools.path import (
    PATH_QUERIES_CONTINENT
)

#################
### Constants ###
#################

BOOL_CREATE_DICT_CONTINENTS = True

#################
### Functions ###
#################

def make_request(query):
    response = requests.get(url=URL_WIKIDATA, params= {'format': 'json', 'query': query})
    data = response.json()
    return data["results"]["bindings"]

def request_countries_continent(code_continent, language:Literal["en", "fr"]="en"):
    wikidata_code_continent = DICT_WIKIDATA_CONTINENTS[code_continent]
    query = """
        SELECT DISTINCT ?country ?countryLabel
        WHERE {
            ?country wdt:P30/wdt:P361* wd:%s.  # `continent` is the desired continent or part of it (recurssively)
            ?country wdt:P31/wdt:P279* wd:Q6256.  # Instance of `country` or any of its subclasses (recurssively)
            ?country wdt:P31/wdt:P279* wd:Q7275.  # Instance of `state` or any of its subclasses (recurssively)

            MINUS {
                ?country wdt:P31/wdt:P279* wd:Q1145276.  # Not instance `fictional country` or any of its subclasses (recurssively)
            }
            MINUS {
                ?country wdt:P31/wdt:P279* wd:Q108762074.  # Not an a fictional state or any of its subclasses (recurssively)
            }
            MINUS {
                ?country wdt:P31/wdt:P279* wd:Q3024240.  # Not an historical country or any of its subclasses (recurssively)
            }
            MINUS {
                ?country wdt:P31/wdt:P279* wd:Q15239622.  # Not a disputed country or any of its subclasses (recurssively)
            }

            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],%s". }
        }
        ORDER BY (?countryLabel)
        """%(wikidata_code_continent, language)

    data = make_request(query)

    dict_results = {}
    for country in data:
        wikidata_code_country = country["country"]["value"].split("/")[-1]
        name_country = country["countryLabel"]["value"]
        if name_country != wikidata_code_country:
            dict_results[wikidata_code_country] = name_country

    save_json_file(
        file_path=PATH_QUERIES_CONTINENT+code_continent+"_"+language+".json",
        dict_to_save=dict_results
    )

def request_official_language(wikidata_code_country, language:Literal["en", "fr"]):
    query = """
    SELECT DISTINCT ?language ?languageLabel
    WHERE {
        wd:%s wdt:P37 ?language.

        MINUS {
            ?language wdt:P31/wdt:P279* wd:Q34228.  # Not an instance of sign language or any of its subclasses
        }

        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],%s". }
        }    
    """%(wikidata_code_country, language)
    data = make_request(query)

    list_languages = []
    for language in data:
        language_name = language["languageLabel"]["value"]
        list_languages.append(language_name.capitalize())
    return list_languages

def format_list_string(list_data):
    """
    Format a list of strings into a string with coma
    
    Parameters
    ----------
    list_data : list[str]
        List of strings to format into a single string.
    
    Returns
    -------
    str
        String containing the elements of the list separated by comas.
    """
    string_data = ""
    for data in list_data:
        string_data += data + ", "
    string_data = string_data[:-2]
    return string_data

def request_clues(code_clue, wikidata_code_country):
    wikidata_language = DICT_WIKIDATA_LANGUAGE[USER_DATA.language]

    if code_clue == "official_language":
        list_data = request_official_language(wikidata_code_country, wikidata_language)
    # TODO mettre les autres requêtes ici pour les autres indices

    string_data = format_list_string(list_data=list_data)
    return string_data

#if __name__ == "__main__":
    #if BOOL_CREATE_DICT_CONTINENTS:
    #    for code_continent in DICT_WIKIDATA_CONTINENTS:
    #        request_countries_continent(code_continent=code_continent, language="en")
    #print(request_clues("official_language", "Q258"))
