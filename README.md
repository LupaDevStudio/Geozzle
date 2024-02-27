# Geozzle

*Geozzle* is a geography quizz using requests to WikiData to gather all available clues for different countries. Players can choose the continent they want to play and attempt to guess all countries within it using as few clues as possible. The objective of the game is simple: collect all countries of each continent.


This game was developped as a school project for the *Connaissances et Raisonnement* class at CentraleSupélec.

The game is available for download on both the PlayStore and the AppStore :

- [Geozzle on the PlayStore](https://play.google.com/store/apps/details?id=lupadevstudio.com.geozzle)
- [Geozzle on the AppStore](https://apps.apple.com/us/app/geozzle/id6478439292)


- [Geozzle](#geozzle)
  - [Installation](#installation)
    - [Cloning the repository](#cloning-the-repository)
    - [Creation of a virtual environment](#creation-of-a-virtual-environment)
    - [Installation of the necessary librairies](#installation-of-the-necessary-librairies)
    - [Launch the code](#launch-the-code)
  - [Utilization](#utilization)
  - [Project organization](#project-organization)
  - [Project architecture](#project-architecture)
  - [Requests to *Wikidata*](#requests-to-wikidata)
    - [Request to get all countries of each continent](#request-to-get-all-countries-of-each-continent)
    - [Request to get all available clues of a country](#request-to-get-all-available-clues-of-a-country)
    - [Clues post-processing](#clues-post-processing)
  - [Graphical interface](#graphical-interface)
  - [Contributors](#contributors)
  - [License](#license)

## Installation

### Cloning the repository

To clone the github repository, you have to search the clone button on the main page of the project. Then click on it and select `https` or `ssh` depending on your favorite mode of connexion. Copy the given id and then open a terminal on your computer, go to the folder where you want to install the project and use the following command:

```bash
git clone <your copied content>
```

### Creation of a virtual environment

You might want to use a virtual environment to execute the code. To do so, use the following command:

```bash
python -m virtualenv venv
```

To start it, use the command on *Windows*:

```bash
./venv/Scripts/Activate.ps1
```

Or for *MacOS* and *Linux*:

```bash
source venv/Scripts/activate
```

### Installation of the necessary librairies

To execute this software, you need several *Python* librairies, specified in the `requirements.txt` file. To install them, use the following command:

```bash
pip install -r requirements.txt
```

### Launch the code

The main code can be launched by running the following command:

```bash
python main.py
```

## Utilization

<table align="center">
    <tr>
        <td align="justify">A tutorial has been written inside the game; when the user launches the game for the first time, the tutorial is displayed. The user can also see it again by clicking on the information button on the bottom-left hand corner of the home screen. 
        The default language is English, but if the player prefers to play in French, they can switch the game language by clicking on the flag button in the top-right corner of the home screen.</td>
        <td align="center"><img src="resources/images/tuto/home_screen_en.png?raw=true" alt="some text" width=800></td>
    </tr>

</table>

## Project organization

When we began working on this project, we initially conceptualized its concept : collecting clues to guess all the countries of a given continent. We then decided on its design and started work on the graphical interface accordingly. 

We conceived the idea of incorporating several picture of famous places for each continent. We used [Stable Diffusion](https://huggingface.co/spaces/prodia/sdxl-stable-diffusion-xl) to generate all of the game images with textual prompts such as "beautiful lavender field, higly render, 4k". All of our generated images are store in the `resources/images` folder.

Additionally, we decided to offer the game in two languages: French and English. Consequently, we created two JSON files (english.json and french.json) in resources/languages. These files contain dictionaries of dictionaries for all continents, pop-ups, tutorials, and clue names. This structure allows us to easily manage language switching within the game.


## Project architecture

The project is divided into several folders:

- `licenses`, containing the different licenses used in this project.
- `resources`, containing the following folders:
  - `fonts`, containing the fonts of the application.
  - `images`, containing all the images used in the application.
  - `languages`, containing the dictionaries of language.
  - `manifest`, containing some tools for the Play Store.
  - `musics`, containing the musics of the game.
  - `queries`, containing some results of the queries to Wikidata. It also contains the module `convert_geojson_to_png.py`, which converted the geojson data into images of the shape of the countries.
  - `sounds`, containing the sound effects of the game.
- `screens`, containing the *Python* modules for the different screens. The subfolder `custom_widgets` contains tools widgets inserted in the screens.
- `tools`, divided into several subfolders and modules:
  - `basic_tools`, folder containing basis tools.
  - `game_tools`, folder containing tools for sounds.
  - `kivy_tools`, folder used for general *Kivy* widgets and functions.
  - `constants.py`, module containing the constants of the application.
  - `geozzle.py`, module containing the main class of the logic of the application.
  - `kivyads.py`, module containing the tools to add ads in the application.
  - `kivyreview.py`, module containig the tools to display the in app review of the game.
  - `path.py`, module containing the constants for the paths.
  - `sparql.py`, module containing the different requests to Wikidata.

It also contains the following files:

- `data.json`, *json* file where are stored the data of the user.
- `.gitignore`
- `main.kv`, *Kivy* module associated to `main.py`.
- `main.py`, main *Python* module of the application.
- `requirements.txt`, list of packages required to run the app.

## Requests to *Wikidata*

All our requests are implemented in Python in the `tools/sparql.py` file. We used two main requests on Wikidata for this game:

- a request to get all countries of each continent
- a request to get all available clues of a country

### Request to get all countries of each continent 

This request is implemented in the `request_countries_continent` function. The results are stored in `resources/queries/continents` in the form of JSON files. We created two files for each continent: one for French and one for English. Each file is a dictionary containing the Wikidata code and name of each country.

This request is created as follow : for a continent, we gather every countries and states, then remove any instance of 'fictional country', 'fictional state', 'historical country', 'disputed country', or any of their subclasses. This allowed us to have the cleanest list of countries with minimal post-processing required.

For our post-processing, we created the `resources/queries/continents/exceptions.json` file. It contains two dictionaries: one for countries to remove (to_remove), which includes the codes of countries to be excluded for each continent, and another for countries to add (to_add), which lists additional codes and country names to include in our JSON files. 

For example, China and Taiwan were excluded in our initial request as they are both disputed countries. We manually added them during the post-processing.

This `exceptions.json` is used in the `request_countries_continent` function (in `sparql.py`) to adjust the lists of countries accordingly.

These JSON files are generated ahead of gaming. You can recreated them by running the sparql.py file, specifying the language argument as either French ('fr') or English ('en').

### Request to get all available clues of a country

This request is employed during gameplay, leading to a short loading time when switching countries. However, it ensures that the clues offered are current and accurate, which was the primary motivation behind its creation.

During gameplay, a country is randomly chosen from the continent the player is currently playing. Then, our second request, written in `HINTS_QUERY` (compressed in `COMPRESSED_HINTS_QUERY`) and implemented in the `request_all_clues` function is used to gather all availables clues for that country. 

| List of all clues |  |  | 
| --- | --- | --- |
| - Official Langage  | - Age of majority | - ISO 3 code (for the country shape) |
| - Anthem  | - Population | - Human development index  |
| - Motto | - Country calling code | -  License plate code|
| - Flag | - Head of state | - Head of government |
| - Capital | - Nominal GPD | -  Internet domain |
| - Area | - Driving side | - Currency |


### Clues post-processing 

#### Removing empty fields

In the post-processing phase of this request, all empty fields are removed, eliminating clues for which there is no value in Wikidata.The `request_all_clues` function returns a dictionary containing all available clues for the selected country.

(A COMPLETER, parler de la dernière update de la requête?)

#### Formatting 
Futher formatting is then realized in the `format_clue` function in `tools/geozzle.py`, for instance the formatting of numbers and the units.

(A COMPLETER, parler de la dernière update de la requête?)

#### The flag image

Displaying flags poses a specific challenge because the request provides a URL to an SVG file. Since SVG files cannot be directly shown using the `kivy` library, we created another request to obtain the corresponding PNG image from the SVG URL. This functionality is implemented in the `download_png_from_svg_url` function within `tools/sparql.py`.

#### Country shape (ISO 3 code)

With the ISO 3 code obtained from the request, we created a python file that convert this geojson file to a PNG file in `extras/convert_geojson_to_png.py`. 

TODO : 1 ou 2 phrases pour dire comment la conversion est faite

The output PNG file contains country shapes that are white with no backgrounds. This format is necessary for displaying the map in our graphical interface, kivy, which can only draw on white spaces. Therefore, having the country shapes in white ensures compatibility with kivy.




The `format_clue`and `request_all_clues` functions are called in the `Game` class defined in `tools/geozzle.py`. The clues are subsequently stored in the `data.json` file along with all other player data including the number of lives, information of the current country (country code, list of current hints), list of already guessed countries, their highscore and more. 


## Graphical interface

TODO : Kivy : fonctionnement kv/python, fonctionnement en écrans managés par un screen manager, fonctionnement avec custom widget, fonctionneent en classes

<table align="center">
    <tr>
        <td align="center">Home Screen</td>
        <td align="center">Game Question Screen</td>
        <td align="center">Game Summary Screen</td>
        <td align="center">Game Over Screen</td>
    </tr>
    <tr>
        <td align="center">home.kv and home.py </td>
        <td align="center">game_question.kv and game_question.py</td>
        <td align="center">game_summary.kv and game_summary.py</td>
        <td align="center">game_over.kv and game_over.py</td>
    </tr>
    <tr>
        <td align="center"><img src="resources/images/tuto/home_screen_en.png?raw=true" alt="some text" width=500></td>
        <td align="center"><img src="resources/images/tuto/game_question_en.png?raw=true" alt="some text" width=500></td>
        <td align="center"><img src="resources/images/tuto/game_summary_en.png?raw=true" alt="some text" width=500></td>
        <td align="center"><img src="resources/images/tuto/game_over_en.png?raw=true" alt="some text" width=500></td>
    </tr>

</table>


## Contributors

This project has been realized by LupaDevStudio, Laure-Emilie Martin and Romain Ageron.

## License

This program is licensed under the `Creative Commons Attribution-NonCommercial-ShareAlike 4.0` license.
