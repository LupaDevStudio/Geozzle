# Geozzle

*Geozzle* is a geography quizz with requests to WikiData in order to get the questions.
ETOFFER UN PEU ICI

- [Geozzle](#geozzle)
  - [Installation](#installation)
    - [Cloning the repository](#cloning-the-repository)
    - [Creation of a virtual environment](#creation-of-a-virtual-environment)
    - [Installation of the necessary librairies](#installation-of-the-necessary-librairies)
    - [Launch the code](#launch-the-code)
  - [Utilisation](#utilisation)
  - [Architecture of the project](#architecture-of-the-project)
  - [Requests to *Wikidata*](#requests-to-wikidata)
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

## Utilisation

<table align="center">
    <tr>
        <td align="justify">A tutorial has been written inside the game and when the user launches the game for the first time, the tutorial is displayed. The user can also see it again by clicking on the information button on the bottom-left hand corner of the home screen.
        The by-default language is english, but the player rather play in french they can switch the game language by clicking on the flag button on the top-right hand corner of the home screen.t</td>
        <td align="center"><img src="resources/images/tuto/home_screen_en.png?raw=true" alt="some text" width=800></td>
    </tr>

</table>
## Architecture of the project

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

TU POURRAS REDIRE OU SE TROUVENT LES REQUETES (résultats des requêtes dans queries de resources, et l'implémentation en Python quand sparql.py de tools) Je l'ai dit dans la partie d'avant mais il y a beaucoup de trucs ^^'
EXPLIQUER ICI LES CHOIX QU'ON A FAITS

## Contributors

This project has been realized by LupaDevStudio, Laure-Emilie Martin and Romain Ageron.

## License

This program is licensed under the `Creative Commons Attribution-NonCommercial-ShareAlike 4.0` license.
