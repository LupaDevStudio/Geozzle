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
    URL_WIKIDATA
)
from tools.path import (
    PATH_QUERIES_CONTINENT,
    PATH_DICT_EXCEPTIONS_COUNTRIES,
    PATH_IMAGES_FLAG
)

#################
### Constants ###
#################

BOOL_CREATE_DICT_CONTINENTS = False

HINTS_QUERY = """
# Replace `$Q_country` with the identifier of the country with the "Q"
# Replace `$output_language` with language of the output, e.g.: `en` for English, `fr` for French, ...


SELECT ?hint ?value ?unit
WITH {
    SELECT DISTINCT ?hint_ ?value_ {
        BIND(wd:$Q_country AS ?country).  # bind `?country` for readability
        BIND(rdfs:label AS ?label_property).  # bind `rdfs:label` for query compression when sending the GET request

        {  # official language
            BIND("official_language" AS ?hint_).

            ?country wdt:P37 ?language.  # official language of the country

            MINUS {
                ?language wdt:P31/wdt:P279* wd:Q34228.  # instance of `sign language` or any of its subclasses
            }

            MINUS {
                ?language wdt:P31/wdt:P279* wd:Q20671156.  # instance of `languages of a geographic region` or any of its subclasses
            }

            ?language ?label_property ?value_.  # do not factor this otherwise the optimizer messes up
        }

        UNION {  # capital
            BIND("capital" AS ?hint_).

            ?country wdt:P36 ?capital.  # force statement to be the preferred statement
            ?country p:P36 ?statement.  # capital statement of the country
            ?statement ps:P36 ?capital.

            OPTIONAL {
                 ?statement pq:P582 ?endtime.  # statement end-time
            }

            FILTER(!BOUND(?endtime)).

            MINUS {
                ?statement pq:P459 wd:Q712144.  # `determination method` is `de facto`
            }
            MINUS {
                ?statement pq:P5102 wd:Q712144.  # `nature of statement` is `de facto`
            }

            ?capital ?label_property ?value_.  # do not factor this otherwise the optimizer messes up
        }

        UNION {  # motto
            BIND("motto" AS ?hint_).

            ?country wdt:P1546 ?motto.  # motto of the country

            ?motto ?label_property ?value_.  # do not factor this otherwise the optimizer messes up
        }

        UNION {  # anthem
            BIND("anthem" AS ?hint_).

            ?country wdt:P85 ?anthem.  # force statement to be the preferred statement
            ?country p:P85 ?statement.  # anthem statement of the country
            ?statement ps:P85 ?anthem.

             OPTIONAL {
                 ?statement pq:P582 ?endtime.  # statement end-time
             }

             FILTER(!BOUND(?endtime)).

            ?anthem ?label_property ?value_.  # do not factor this otherwise the optimizer messes up
        }

        UNION {  # top level internet domain
            BIND("top_level_internet_domain" AS ?hint_).

            ?country wdt:P78 ?domain.  # top level internet domain of the country

            ?domain ?label_property ?value_.  # do not factor this otherwise the optimizer messes up
        }

        UNION {  # driving side
            BIND("driving_side" AS ?hint_).

            ?country wdt:P1622 ?side.  # driving side in the country

            ?side ?label_property ?value_.  # do not factor this otherwise the optimizer messes up
        }

        UNION {  # currency
            BIND("currency" AS ?hint_).

            ?country wdt:P38 ?currency.  # currency of the country

            ?currency ?label_property ?value_.  # do not factor this otherwise the optimizer messes up
        }

        UNION {  # head of state
            BIND("head_of_state" AS ?hint_).

            ?country wdt:P35 ?head_of_state.  # head of state of the country

            ?head_of_state ?label_property ?value_.  # do not factor this otherwise the optimizer messes up
        }

        UNION {  # head of government
            BIND("head_of_government" AS ?hint_).

            ?country wdt:P6 ?head_of_government.  # force statement to be the preferred statement
            ?country p:P6 ?statement.  # head of government statement of the country
            ?statement ps:P6 ?head_of_government.

            OPTIONAL {
                 ?statement pq:P582 ?endtime.  # statement end-time
            }

            FILTER(!BOUND(?endtime)).

            ?head_of_government ?label_property ?value_.  # do not factor this otherwise the optimizer messes up
        }

        # requires using `rdfs:label`, does not work with `SERVICE  wikibase:label { ... }`
        FILTER(LANG(?value_) = "$output_language").  # filter the language of the labels
        FILTER(!REGEX(?value_, "^Q[1-9][0-9]*$")).  # do not take the label if it is the identifier of the entity
    }
} AS %entity_valued_hints

WITH {
    SELECT DISTINCT ?hint_ ?value_ {
        BIND(wd:$Q_country AS ?country).  # bind `?country` for readability

        {  # flag
              BIND("flag" AS ?hint_).
              BIND(?flag AS ?value_).

              ?country wdt:P41 ?flag.  # flag image of the country
        }

        UNION {  # age of majority
            BIND("age_of_majority" AS ?hint_).
            BIND(?age AS ?value_).

            ?country wdt:P2997 ?age.  # force statement to be the preferred statement
            ?country p:P2997 ?statement.  # age of majority statement of the country
            ?statement ps:P2997 ?age.

            OPTIONAL {
                 ?statement pq:P582 ?endtime.  # statement end-time
            }

            FILTER(!BOUND(?endtime)).
        }

        UNION {  # human development index
            BIND("human_development_index" AS ?hint_).
            BIND(?hdi AS ?value_).

            ?country wdt:P1081 ?hdi.  # human development index of the country
        }

        UNION {  # population
            BIND("population" AS ?hint_).
            BIND(?population AS ?value_).

            ?country wdt:P1082 ?population.  # population of the country
        }

        UNION {  # country calling code
            BIND("country_calling_code" AS ?hint_).
            BIND(?code AS ?value_).

            ?country wdt:P474 ?code.  # calling code of the country
        }

        UNION {  # ISO 3166-1 alpha-2 code
            BIND("ISO_2_code" AS ?hint_).
            BIND(?code AS ?value_).

            ?country wdt:P297 ?code.  # ISO 3166-1 alpha-2 code of the country
        }

        UNION {  # ISO 3166-1 alpha-3 code
            BIND("ISO_3_code" AS ?hint_).
            BIND(?code AS ?value_).

            ?country wdt:P298 ?code.  # ISO 3166-1 alpha-3 code of the country
        }

        UNION {  # license plate code
            BIND("license_plate_code" AS ?hint_).
            BIND(?code AS ?value_).

            ?country wdt:P395 ?code.  # license plate code of the country
        }

        FILTER(?hint_ = "flag" || !isIRI(?value_)).  # except for the flag, verify that the value is not an IRI (mostly the case for "unknown value")
    }
} AS %dimensionless_valued_hints

WITH {
    SELECT DISTINCT ?hint_ ?value_ ?unit {
        BIND(wd:$Q_country AS ?country).  # bind `?country` for readability
        BIND(rdfs:label AS ?label_property).  # bind `rdfs:label` for query compression when sending the GET request

        {  # area in km^2
            BIND("area" AS ?hint_).
            BIND(?area AS ?value_).
            BIND(wd:Q712226 AS ?unit_).  # output in km^2

            ?country wdt:P2046 ?wd_area.  # force statement to be the preferred statement
            ?country p:P2046 ?statement. # area of the country

            ?statement psv:P2046 ?wd_value_node.  # get the value node
            ?wd_value_node wikibase:quantityAmount ?wd_area.  # link value node to preferred statement

            ?statement psn:P2046 ?si_value_node.  # get the value node in SI unit
            ?si_value_node wikibase:quantityAmount ?si_area.  # area value in SI unit

            ?unit_ wdt:P2370 ?si_conv.  # conversion factor to SI unit (m^2)

            BIND((?si_area / ?si_conv) AS ?area).  # conversion from SI unit (m^2) to output unit

            ?unit_ ?label_property ?unit_label.  # do not factor this otherwise the optimizer messes up
        }

        UNION {  # nominal GDP
            BIND("nominal_GDP" AS ?hint_).
            BIND(?gdp AS ?value_).

            ?country wdt:P2131 ?gdp.  # force statement to be the preferred statement
            ?country p:P2131 ?statement.  # nominal GDP of the country

            ?statement psv:P2131 ?value_node.  # get the value node
            ?value_node wikibase:quantityAmount ?gdp.  # get the gdp value
            ?value_node wikibase:quantityUnit ?unit_.  # get the gdp unit

            ?unit_ ?label_property ?unit_label.  # do not factor this otherwise this optimizer messes up
        }

        FILTER(!isIRI(?value_)).  # verify that the value is not an IRI (mostly the case for "unknown value")

        FILTER(LANG(?unit_label) = "$output_language").  # filter the language of the labels
        FILTER(!REGEX(?unit_label, "^Q[1-9][0-9]*$")).  # do not take the label if it is the identifier of the unit

        BIND (  # custom abbreviations for most common units
            COALESCE(
                IF(?unit_ = wd:Q712226, "km²", 1/0),
                IF(?unit_ = wd:Q4917, "$", 1/0),
                IF(?unit_ = wd:Q4916, "€", 1/0),
                IF(?unit_ = wd:Q25224, "£", 1/0),
                IF(?unit_ = wd:Q1104069, "CA-$", 1/0),
                ?unit_label
            ) AS ?unit
        ).
    }
} AS %dimension_valued_hints

WHERE {
    {
        INCLUDE %entity_valued_hints.
    } UNION {
        INCLUDE %dimensionless_valued_hints.
    } UNION {
        INCLUDE %dimension_valued_hints.
    }

    BIND(?hint_ AS ?hint).  # Use private names for query compression when sending the GET request
    BIND(?value_ AS ?value).  # Use private names for query compression when sending the GET request
}
"""

COMPRESSED_HINTS_QUERY = (
    " ".join(
        filter(
            None,
            map(
                lambda line: line.split("#")[0].strip(),
                HINTS_QUERY.splitlines(),
            ),
        )
    )
    .replace(" {", "{")
    .replace("{ ", "{")
    .replace(" }", "}")
    .replace("} ", "}")
    .replace(" (", "(")
    .replace("( ", "(")
    .replace(" )", ")")
    .replace(") ", ")")
    .replace(". ", ".")
    .replace(" .", ".")
    .replace(", ", ",")
    .replace(" ,", ",")
    .replace("= ", "=")
    .replace(" =", "=")
    .replace("?hint_", "?z")
    .replace("?value_", "?y")
    .replace("?label_property", "?x")
    .replace("?unit_", "?w")
    .replace("?country", "?v")
    .replace("%entity_valued_hints", "%z")
    .replace("%dimensionless_valued_hints", "%y")
    .replace("%dimension_valued_hints", "%x")
)


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

    dict_results = dict(sorted(dict_results.items(), key=lambda item: item[1]))

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
    for data, unit in list_data:
        string_data += data
        if unit:
            string_data += f" {unit}"
        string_data += ", "
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
        value_hint = item["value"]["value"]
        unit_hint = item["unit"]["value"] if "unit" in item else ""

        # Sort by hint
        if type_hint not in dict_all_clues:
            dict_all_clues[type_hint] = []
        dict_all_clues[type_hint].append((value_hint, unit_hint))

    hints_to_delete = []

    # Format the list into string
    for type_hint in dict_all_clues:
        if type_hint != "flag":
            dict_all_clues[type_hint] = format_list_string(list_data=dict_all_clues[type_hint])
        else:
            has_success = post_treat_flag(dict_all_clues[type_hint][0][0], code_continent)
            if not has_success:
                hints_to_delete.append(type_hint)
            else:
                dict_all_clues[type_hint] = "flag_" + code_continent.lower() + ".png"

    for type_hint in hints_to_delete:
        del dict_all_clues[type_hint]

    return dict_all_clues

def request_all_clues(wikidata_code_country: str, code_continent: str, language):
    query = (
        COMPRESSED_HINTS_QUERY
             .replace("$Q_country", wikidata_code_country)
             .replace("$output_language", language)
    )

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
    if BOOL_CREATE_DICT_CONTINENTS:
       for code_continent in DICT_WIKIDATA_CONTINENTS:
           request_countries_continent(code_continent=code_continent, language="fr")
    print(request_all_clues("Q236", "Europe", "english"))
