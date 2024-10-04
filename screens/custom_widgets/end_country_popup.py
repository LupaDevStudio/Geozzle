"""
Module to create a popup to allow the user to regenerate lives.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.properties import (
    ObjectProperty,
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ColorProperty
)
from kivy.uix.relativelayout import RelativeLayout

### Local imports ###

from screens.custom_widgets.custom_popup import CustomPopup
from tools.geozzle import (
    TEXT
)
from tools.constants import (
    BLACK,
    WHITE,
    DICT_CONTINENT_SECOND_COLOR,
    DICT_CONTINENTS_PRIMARY_COLOR
)

#############
### Class ###
#############


class EndCountryPopup(CustomPopup):
    
    popup_size = ObjectProperty((0.85, 0.45))
    ok_button_label = StringProperty(TEXT.popup["close"])
    score_text = StringProperty()
    release_function = ObjectProperty(lambda: 1 + 1)

    country_name = StringProperty()
    multiplier_image = StringProperty()
    new_image = StringProperty()
    nb_stars = NumericProperty()
    flag_image = StringProperty()

    def confirm(self):
        self.dismiss()
        self.release_function()

class CountryLineScore(RelativeLayout):
    font_ratio = NumericProperty(0)
    country_name = StringProperty()
    flag_image = StringProperty()
    flag_color = ColorProperty(WHITE)
    nb_stars = NumericProperty(0)
    continent_color = ColorProperty(BLACK)

    text_label = StringProperty()
    score_label = StringProperty()

class EndGamePopup(CustomPopup):

    # {"code_continent": {
        # "country_name": str,
        # "guessed": bool,
        # "score_clues": int,
        # "flag_image": str,
        # "nb_stars": str,
        # "multiplier": str}}
    dict_score_details_countries = ObjectProperty({})

    number_lives_at_the_end_label = StringProperty()
    number_lives_at_the_end = NumericProperty(0)
    total_score_label = StringProperty()
    total_score = NumericProperty(0)

    guessed_label = StringProperty()
    clues_label = StringProperty()
    multiplier_label = StringProperty()
    total_label = StringProperty()

    release_function = ObjectProperty(lambda: 1 + 1)
    ok_button_label = StringProperty(TEXT.popup["close"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(dict_score_details_countries=self.rebuild_scrollview)
        self.rebuild_scrollview()

    def build_scrollview(self):
        total_score = 0
        scrollview_layout = self.ids.scrollview_layout
        text_label = self.guessed_label + "\n" + self.clues_label + "\n" + \
            self.multiplier_label + "\n" + self.total_label
        
        for code_continent in self.dict_score_details_countries:
            dict_details = self.dict_score_details_countries[code_continent]
            continent_color = DICT_CONTINENTS_PRIMARY_COLOR[code_continent]
            score_guessed = 100 if dict_details["guessed"] else 0
            score_clues = dict_details["score_clues"]
            multiplier = dict_details["multiplier"]
            total_score_country = int((score_guessed + score_clues) * multiplier)
            total_score += total_score_country
            
            # Format well the multiplier
            if multiplier in [float(1), float(2)]:
                multiplier = int(multiplier)
            
            # Label for the score
            score_label = str(score_guessed) + "\n" + str(score_clues) + "\n" + \
                str(multiplier) + "\n" + str(total_score_country)
            
            country_layout = CountryLineScore(
                font_ratio=self.font_ratio,
                size_hint=(1, None),
                height=90*self.font_ratio,
                flag_color=dict_details["flag_color"],
                continent_color=continent_color,
                country_name=dict_details["country_name"],
                score_label=score_label,
                text_label=text_label,
                nb_stars=dict_details["nb_stars"],
                flag_image=dict_details["flag_image"]
            )
            scrollview_layout.add_widget(country_layout)
        
        total_score += self.number_lives_at_the_end * 150
        # Verify the total score is correct at the end
        if self.total_score != total_score:
            print("La fonction de calcul de score est fausse")
            print("TOTAL SCORE", self.total_score)
            print("TOTAL SCORE CALCULE", total_score)

    def rebuild_scrollview(self, *args):
        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        # Build scrollview
        self.build_scrollview()

    def confirm(self):
        self.dismiss()
        self.release_function()
