"""
Module to create the game screen with the summary of all clues.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.properties import (
    StringProperty,
    ColorProperty,
    NumericProperty
)
from kivy.uix.label import Label

### Local imports ###

from tools.path import (
    PATH_BACKGROUNDS,
    PATH_TEXT_FONT
)
from tools.constants import (
    DICT_CONTINENTS,
    LIST_CONTINENTS,
    DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED,
    TEXT
)
from tools.kivy_tools import ImprovedScreen

#############
### Class ###
#############


class GameSummaryScreen(ImprovedScreen):
        
    code_continent = StringProperty(LIST_CONTINENTS[0])
    continent_color = ColorProperty(DICT_CONTINENTS[LIST_CONTINENTS[0]])
    background_color = ColorProperty(DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[LIST_CONTINENTS[0]])
    number_lives_on = NumericProperty(3)
    dict_all_clues = {}
    dict_scrollview_widgets = {}
    text_found_country = StringProperty() 
    get_new_hint = StringProperty()
    title_label = StringProperty()


    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=PATH_BACKGROUNDS + "lake_sunset.jpg",
            font_name=PATH_TEXT_FONT,
            **kwargs)
        
        self.bind(code_continent = self.update_color)
        self.update_text()

    def on_pre_enter(self, *args):
        self.update_scroll_view()
        self.update_text()
        return super().on_pre_enter(*args)

    def update_text(self):
        """
        Update the labels depending on the language.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """
        self.text_found_country = TEXT.game_summary["i_found"]
        self.get_new_hint = TEXT.game_summary["new_hint"]
        self.title_label = TEXT.game_summary["title"]

    def reset_screen(self):
        self.ids.scrollview_layout.reset_screen()
        self.dict_scrollview_widgets = {}
        self.dict_all_clues = {
            "toGG4 erazqg'3G4o": "Superficie : 400km²",
            "tofzfzfe za Gjfg": "Population : 1,000,000",
            "toGG4dzdz3G4o": "Superficie : 400km²",
            "tofzfzdzdza Gjfg": "Population : 1,000,000",
            "toGGdzdz43G4o": "Superficie : 400km²",
            "tofzcqcfza Gjfg": "Population : 1,000,000",
            "toGGvdvd43G4o": "Superficie : 400km²",
            "tofzfzvdsva Gjfg": "Population : 1,000,000",
            "toGG cx43G4o": "Superficie : 400km²",
            "tofzfzeveqze a Gjfg": "Population : 1,000,000",
            "toGG43f ezG4o": "Superficie : 400km²",
            "tofzfza f efeGjfg": "Population : 1,000,000"
        }

    def update_scroll_view(self):
        """
        Add the labels of clues in the scrollview.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for key in self.dict_all_clues:

            # Add the labels which are not already in the scrollview
            if not key in self.dict_scrollview_widgets:
                label_clue = Label(
                    text="– " + self.dict_all_clues[key],
                    color=self.continent_color,
                    font_name=self.font_name,
                    font_size=20*self.font_ratio,
                    halign="left",
                    valign="middle",
                    shorten=False,
                    line_height=1
                )
                label_clue.bind(texture_size=label_clue.setter('size'))
                label_clue.bind(size=label_clue.setter('text_size'))
                self.ids.scrollview_layout.add_widget(label_clue)

                self.dict_scrollview_widgets[key] = label_clue

    def update_color(self, base_widget, value):
        """
        Update the code of the continent and its related attributes.

        Parameters
        ----------
        base_widget : kivy.uix.widget
            Self
        value : string
            Value of code_continent

        Returns
        -------
        None
        """
        self.continent_color = DICT_CONTINENTS[self.code_continent]
        self.background_color = DICT_CONTINENT_THEME_BUTTON_BACKGROUND_COLORED[self.code_continent]

    def go_to_game_over(self):
        self.manager.current = "game_over"

    def go_to_game_question(self):
        self.manager.current = "game_question"

    def go_back_to_home(self):
        self.manager.current = "home"
