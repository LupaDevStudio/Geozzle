###############
### Imports ###
###############

### Python imports ###

import requests
import sys
sys.path.append("../")
sys.path.append("./")

### Local imports ###

from tools.basic_tools.json import (
    save_json_file
)

from tools.constants import (
    DICT_WIKIDATA_CONTINENTS,
    URL_WIKIDATA
)

from tools.path import (
    PATH_QUERIES_CONTINENT
)

#################
### Functions ###
#################

def request_countries_continent(code_continent, language="en"):
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
        """%(wikidata_code_continent, language)

    response = requests.get(url=URL_WIKIDATA, params= {'format': 'json', 'query': query})
    data = response.json()

    data = data["results"]["bindings"]
    dict_results = {}
    for country in data:
        wikidata_code_country = country["country"]["value"].split("/")[-1]
        name_country = country["countryLabel"]["value"]
        dict_results[wikidata_code_country] = name_country

    save_json_file(
        file_path=PATH_QUERIES_CONTINENT+code_continent+"_"+language+".json",
        dict_to_save=dict_results
    )

if __name__ == "__main__":
    for code_continent in DICT_WIKIDATA_CONTINENTS:
        request_countries_continent(code_continent=code_continent, language="fr")
