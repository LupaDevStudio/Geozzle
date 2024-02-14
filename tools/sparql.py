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

def download_png_from_svg_url(svg_url: str, code_continent: str):
    try:
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

        url = png_url

        headers = {
            'User-Agent': 'Geozzle/1.0 (https://lupadevstudio.com; lupa.dev.studio@gmail.com) python-requests/2.28.2'}

        response = requests.get(url, headers=headers, stream=True)
        with open(PATH_IMAGES_FLAG + code_continent.lower() + ".png", 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        # del response
        return True
    except:
        print("No connection")
        return False

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

def post_treat_flag(svg_url, code_continent):
    try:
        has_success = download_png_from_svg_url(svg_url, code_continent)
        return has_success
    except:
        return False

def post_treat_request(data, code_continent: str):
    dict_all_clues = {}

    for item in data:
        type_hint = item["hint"]["value"]
        value_hint = item["valueLabel"]["value"]

        # Sort by hint
        if not type_hint in dict_all_clues:
            dict_all_clues[type_hint] = []
        dict_all_clues[type_hint].append(value_hint)

    hints_to_delete = []

    # Format the list into string
    for type_hint in dict_all_clues:
        if type_hint != "flag":
            dict_all_clues[type_hint] = format_list_string(list_data=dict_all_clues[type_hint])
        else:
            has_success = post_treat_flag(dict_all_clues[type_hint][0], code_continent)
            if not has_success:
                hints_to_delete.append(type_hint)
            else:
                dict_all_clues[type_hint] = "flag_" + code_continent.lower() + ".png"

    for type_hint in hints_to_delete:
        del dict_all_clues[type_hint]

    return dict_all_clues

def request_all_clues(wikidata_code_country: str, code_continent: str, language = DICT_WIKIDATA_LANGUAGE[USER_DATA.language]):
    query = """
    SELECT DISTINCT ?hint ?valueLabel
    WHERE {
        BIND(wd:%s AS ?country)

        {  # official language
            BIND("official_language" AS ?hint)
            BIND(?language AS ?value)

            ?country wdt:P37 ?language.  # official language of the country

            MINUS {
                ?language wdt:P31/wdt:P279* wd:Q34228.  # instance of `sign language` or any of its subclasses
            }

            MINUS {
                ?language wdt:P31/wdt:P279* wd:Q20671156.  # instance of `languages of a geographic region` or any of its subclasses
            }
        }

        UNION {  # capital
            BIND("capital" AS ?hint)
            BIND(?capital AS ?value)

            ?country wdt:P36 ?capital.  # force statement to be the main statement
            ?country p:P36 ?statement.  # capital statement of the country
            ?statement ps:P36 ?capital.

            OPTIONAL {
                ?statement pq:P582 ?endtime.  # statement end-time
            }

            FILTER(!bound(?endtime))

            MINUS {
                ?statement pq:P459 wd:Q712144.  # `determination method` is `de facto`
            }
            MINUS {
                ?statement pq:P5102 wd:Q712144.  # `nature of statement` is `de facto`
            }
        }

        UNION {  # motto
            BIND("motto" AS ?hint)
            BIND(?motto AS ?value)

            ?country wdt:P1546 ?motto.  # motto of the country
        }

        UNION {  # anthem
            BIND("anthem" AS ?hint)
            BIND(?anthem AS ?value)

            ?country p:P85 ?statement.  # anthem statement of the country
            ?statement ps:P85 ?anthem.

            OPTIONAL {
                ?statement pq:P582 ?endtime.  # statement end-time
            }

            FILTER(!bound(?endtime))
        }

        UNION {  # flag
            BIND("flag" AS ?hint)
            BIND(?flag AS ?value)

            ?country wdt:P41 ?flag.  # flag image of the country
        }

        UNION {  # age of majority
            BIND("age_of_majority" AS ?hint)
            BIND(?age AS ?value)

            ?country wdt:P2997 ?age.  # age of majority of the country
        }

        UNION {  # human development index
            BIND("human_development_index" AS ?hint)
            BIND(?hdi AS ?value)

            ?country wdt:P1081 ?hdi.  # human development index of the country
        }

        UNION {  # population
            BIND("population" AS ?hint)
            BIND(?population AS ?value)

            ?country wdt:P1082 ?population.  # population of the country
        }

        UNION {  # median income
            BIND("median_income" AS ?hint)
            BIND(?income AS ?value)

            ?country wdt:P3529 ?income.  # median income of the country
        }

        UNION {  # area
            BIND("area" AS ?hint)
            BIND(?area AS ?value)

            ?country wdt:P2046 ?area.  # area of country
        }

        UNION {  # country calling code
            BIND("country_calling_code" AS ?hint)
            BIND(?code AS ?value)

            ?country wdt:P474 ?code.  # calling code of the country
        }

        UNION {  # license plate code
            BIND("license_plate_code" AS ?hint)
            BIND(?code AS ?value)

            ?country wdt:P395 ?code.  # license plate code of the country
        }

        UNION {  # nominal GDP
            BIND("nominal_GDP" AS ?hint)
            BIND(?gdp AS ?value)

            ?country wdt:P2131 ?gdp.  # nominal GDP of the country
        }

        UNION {  # top level internet domain
            BIND("top_level_internet_domain" AS ?hint)
            BIND(?domain AS ?value)

            ?country wdt:P78 ?domain.  # top level internet domain of the country
        }

        UNION {  # ISO 3166-1 alpha-2 code
            BIND("ISO_2_code" AS ?hint)
            BIND(?code AS ?value)

            ?country wdt:P297 ?code.  # ISO 3166-1 alpha-2 code of the country
        }

        UNION {  # ISO 3166-1 alpha-3 code
            BIND("ISO_3_code" AS ?hint)
            BIND(?code AS ?value)

            ?country wdt:P298 ?code.  # ISO 3166-1 alpha-3 code of the country
        }

        UNION {  # driving side
            BIND("driving_side" AS ?hint)
            BIND(?side AS ?value)

            ?country wdt:P1622 ?side.  # driving side in the country
        }

        UNION {  # currency
            BIND("currency" AS ?hint)
            BIND(?currency AS ?value)

            ?country wdt:P38 ?currency.  # currency of the country
        }

        UNION {  # head of state
            BIND("head_of_state" AS ?hint)
            BIND(?head_of_state AS ?value)

            ?country wdt:P35 ?head_of_state.  # head of state of the country
        }

        UNION {  # head of government
            BIND("head_of_government" AS ?hint)
            BIND(?head_of_government AS ?value)

            ?country wdt:P6 ?head_of_government.  # head of government of the country
        }

        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],%s". }
    }
    """%(wikidata_code_country, language)

    data = make_request(query)

    # Try a second time the request if fails the first time
    if data is None:
        data = make_request(query)
        if data is None:
            return

    # Post treat the output of the request (by removing empty fields)
    dict_all_clues = post_treat_request(data=data, code_continent=code_continent)

    return dict_all_clues

if __name__ == "__main__":
    # if BOOL_CREATE_DICT_CONTINENTS:
    #    for code_continent in DICT_WIKIDATA_CONTINENTS:
    #        request_countries_continent(code_continent=code_continent, language="en")
    print(request_all_clues("Q1013", "Africa"))
