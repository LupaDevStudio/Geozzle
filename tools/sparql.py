###############
### Imports ###
###############

### Python imports ###

import requests
import sys
import shutil
sys.path.append("../")
sys.path.append("./")
from typing import Literal

### Local imports ###

from tools.basic_tools.json import (
    save_json_file,
    load_json_file
)

from tools.constants import (
    DICT_WIKIDATA_CONTINENTS,
    DICT_WIKIDATA_LANGUAGE,
    URL_WIKIDATA,
    USER_DATA
)

from tools.path import (
    PATH_QUERIES_CONTINENT,
    PATH_DICT_EXCEPTIONS_COUNTRIES,
    PATH_IMAGES_FLAG
)

#################
### Constants ###
#################

BOOL_CREATE_DICT_CONTINENTS = True

#################
### Functions ###
#################

def make_request(query):
    try:
        response = requests.get(
            url=URL_WIKIDATA,
            params= {'format': 'json', 'query': query},
            timeout=5)
        data = response.json()
        return data["results"]["bindings"]
    except:
        print("No connection")
        return

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
    if data is None:
        return

    dict_results = {}
    for country in data:
        wikidata_code_country = country["country"]["value"].split("/")[-1]
        name_country = country["countryLabel"]["value"]
        if name_country != wikidata_code_country:
            dict_results[wikidata_code_country] = name_country

    # Correct the list of countries
    dict_exception = load_json_file(PATH_DICT_EXCEPTIONS_COUNTRIES)
    for country in dict_exception["to_remove"][code_continent]:
        if country in dict_results:
            del dict_results[country]
    for country in dict_exception["to_add"][code_continent]:
        if language == "en":
            dict_results[country[0]] = country[1]
        else:
            dict_results[country[0]] = country[2]

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

    # Try a second time the request
    if data is None:
        data = make_request(query)
        if data is None:
            return

    list_languages = []
    for language in data:
        language_name = language["languageLabel"]["value"]
        list_languages.append(language_name.capitalize())
    return list_languages

def download_png_from_svg_url(svg_url: str, code_continent: str):
    try:
        print("URL", svg_url)
        svg_url = svg_url.replace("Special:FilePath/", "File:")
        response = requests.get(
            url=svg_url,
            timeout=5)
        data = response.text
        extracted_data = data
        end_mark = data.find("Original file</a>") + len("Original file</a>")
        cut_data = data[:end_mark]
        begin_mark = cut_data.rfind("<a")
        extracted_data = data[begin_mark:end_mark]

        segments = extracted_data.split(" ")
        for segment in segments:
            if "href" in segment:
                result = segment[:-1].replace('href="', "")
                break

        name = result.split("/")[-1]

        png_url = result + f"/512px-{name}.png"

        png_url = png_url.replace("https://upload.wikimedia.org/wikipedia/commons/",
                                  "https://upload.wikimedia.org/wikipedia/commons/thumb/")
        # print(png_url)

        url = png_url

        headers = {
            'User-Agent': 'Geozzle/1.0 (https://lupadevstudio.com; lupa.dev.studio@gmail.com) python-requests/2.28.2'}

        response = requests.get(url, headers=headers, stream=True)
        # print(response.status_code)
        # print(response.text)
        with open(PATH_IMAGES_FLAG + code_continent.lower() + ".png", 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        # del response
        return True
    except:
        print("No connection")
        return False

def request_country_flag(wikidata_code_country, language:Literal["en", "fr"], code_continent:str):
    query = """
    SELECT DISTINCT ?flag
    WHERE {
        wd:%s wdt:P41 ?flag.

    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],%s". }
    }
    """%(wikidata_code_country, language)

    data = make_request(query)

    # Try a second time the request
    if data is None:
        data = make_request(query)
        if data is None:
            return
    
    try:
        url = data[0]["flag"]["value"]
        has_success = download_png_from_svg_url(url, code_continent)
        return has_success
    except:
        return False

def request_motto(wikidata_code_country, language:Literal["en", "fr"]):
    query = """
    SELECT DISTINCT ?mottoLabel
    WHERE {
        wd:%s wdt:P1546 ?motto.

    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],%s". }
    }"""%(wikidata_code_country, language)

    data = make_request(query)

    # Try a second time the request
    if data is None:
        data = make_request(query)
        if data is None:
            return
        
    list_mottos = []
    for motto in data:
        motto_name = motto["mottoLabel"]["value"]
        list_mottos.append(motto_name)
    return list_mottos

def request_anthem(wikidata_code_country, language:Literal["en", "fr"]):
    query = """
    SELECT DISTINCT ?anthem ?anthemLabel
    WHERE {
        wd:%s p:P85 ?statement.
        ?statement ps:P85 ?anthem.

        OPTIONAL {
            ?statement pq:P582 ?endtime.
        }
    FILTER(!bound(?endtime))
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],%s". }
    }"""%(wikidata_code_country, language)

    data = make_request(query)

    # Try a second time the request
    if data is None:
        data = make_request(query)
        if data is None:
            return
        
    list_anthems = []
    for anthem in data:
        anthem_name = anthem["anthemLabel"]["value"]
        list_anthems.append(anthem_name)
    return list_anthems

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
    if len(list_data) >= 5:
        list_data = list_data[:5]
    string_data = ""
    for data in list_data:
        string_data += data + ", "
    string_data = string_data[:-2]
    return string_data

def request_clues(code_clue: str, wikidata_code_country: str, code_continent: str):
    wikidata_language = DICT_WIKIDATA_LANGUAGE[USER_DATA.language]
    list_data = []

    if code_clue == "official_language":
        list_data = request_official_language(wikidata_code_country, wikidata_language)
    if code_clue == "flag":
        has_success = request_country_flag(wikidata_code_country, wikidata_language, code_continent)
        return has_success
    if code_clue == "motto":
        list_data = request_motto(wikidata_code_country, wikidata_language)
    if code_clue == "anthem":
        list_data = request_anthem(wikidata_code_country, wikidata_language)
    # TODO mettre les autres requêtes ici pour les autres indices

    # If the request fails
    if list_data is None:
        return

    string_data = format_list_string(list_data=list_data)
    return string_data

if __name__ == "__main__":
    if BOOL_CREATE_DICT_CONTINENTS:
        for code_continent in DICT_WIKIDATA_CONTINENTS:
            request_countries_continent(code_continent=code_continent, language="fr")
    # print(request_clues("official_language", "Q865", "Europe"))
