"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

import random as rd
from threading import Thread

### Kivy imports ###

from kivy.properties import (
    StringProperty
)
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT
)
from screens.custom_widgets import (
    GeozzleScreen,
    MyScrollViewLayout
)
from tools.constants import (
    DICT_MEDALS,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP,
    SUB_TEXT_FONT_SIZE,
    WHITE,
    BLACK
)
from tools.geozzle import (
    USER_DATA,
    TEXT,
    SHARED_DATA
)

#############
### Class ###
#############


class WorldRankingScreen(GeozzleScreen):

    highscore_label = StringProperty()

    dict_type_screen = {
        SCREEN_TITLE: {
            "title": "world_ranking"
        },
        SCREEN_ICON_LEFT_UP: {}
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(
            back_image_path=rd.choice(SHARED_DATA.list_unlocked_backgrounds),
            font_name=PATH_TEXT_FONT,
            **kwargs)

    def reload_language(self):
        """
        Update the labels depending on the language.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        super().reload_language()
        self.highscore_label = TEXT.stats["highscore"].replace(
            "[HIGHSCORE]", str(USER_DATA.highscore))
        if USER_DATA.db_info["ranking"] is not None:
            self.highscore_label += "\n" + TEXT.home["ranking"].replace(
                    "[RANK]", str(USER_DATA.db_info["ranking"]))

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def fill_list_scores_to_display(self, list_scores_to_display, lower_bound, upper_bound):
        for counter in range(lower_bound, upper_bound):
            list_scores_to_display.append(
                {
                    "rank": counter + 1,
                    "score": USER_DATA.db_info["world_ranking"][counter]["score"]
                })
        return list_scores_to_display

    def fill_scrollview(self):
        scrollview_layout: MyScrollViewLayout = self.ids.scrollview_layout

        list_scores_to_display = []

        MAX_NUMBER_TO_DISPLAY = 30
        NUMBER_TO_DISPLAY_AROUND = 10

        # If there are less than 30 scores, display all scores
        if len(USER_DATA.db_info["world_ranking"]) <= MAX_NUMBER_TO_DISPLAY or USER_DATA.db_info["ranking"] is None:
            list_scores_to_display = self.fill_list_scores_to_display(
                list_scores_to_display=list_scores_to_display,
                lower_bound=0,
                upper_bound=len(USER_DATA.db_info["world_ranking"])
            )
        # Else, display the ten firsts, then the ten above the user and the ten after the user
        else:
            # Fill the 30 first scores if the user is in the 20 firsts
            if USER_DATA.db_info["ranking"] <= 2*NUMBER_TO_DISPLAY_AROUND:
                list_scores_to_display = self.fill_list_scores_to_display(
                    list_scores_to_display=list_scores_to_display,
                    lower_bound=0,
                    upper_bound=MAX_NUMBER_TO_DISPLAY
                )
            else:
                # Fill the ten first players
                list_scores_to_display = self.fill_list_scores_to_display(
                    list_scores_to_display=list_scores_to_display,
                    lower_bound=0,
                    upper_bound=NUMBER_TO_DISPLAY_AROUND
                )
                # For the three dots of separation
                list_scores_to_display.append({})
                # Fill the ten players before and after the user
                list_scores_to_display = self.fill_list_scores_to_display(
                    list_scores_to_display=list_scores_to_display,
                    lower_bound=USER_DATA.db_info["ranking"]-1-NUMBER_TO_DISPLAY_AROUND,
                    upper_bound=min(USER_DATA.db_info["ranking"]+NUMBER_TO_DISPLAY_AROUND, len(USER_DATA.db_info["world_ranking"]))
                )

        # Add the labels in the scrollview
        for dict_details in list_scores_to_display:
            if dict_details != {}:
                rank = dict_details["rank"]
                score = dict_details["score"]
                color = BLACK
                if USER_DATA.db_info["ranking"] == rank:
                    color = self.continent_color
                height = 25*self.font_ratio
                relative_layout = RelativeLayout(
                    size_hint=(1, None),
                    height=height
                )

                ### Rank label ###
                rank_label = Label(
                    text=str(rank),
                    font_name=self.font_name,
                    font_size=SUB_TEXT_FONT_SIZE * self.font_ratio,
                    size_hint=(1, 1),
                    halign="left",
                    valign="middle",
                    color=color,
                    outline_width=1*self.font_ratio,
                    outline_color=WHITE
                )
                rank_label.bind(size=rank_label.setter('text_size'))
                relative_layout.add_widget(rank_label)

                ### Rank image for the three first ones ###
                if rank <= 3:
                    rank_image = Image(
                        source=DICT_MEDALS[rank],
                        size_hint=(None, 1),
                        width=height,
                        pos_hint={"center_y": 0.5},
                        x=height+1*self.font_ratio
                    )
                    relative_layout.add_widget(rank_image)

                ### Score label ###
                score_label = Label(
                    text=str(score),
                    font_name=self.font_name,
                    font_size=SUB_TEXT_FONT_SIZE * self.font_ratio,
                    size_hint=(1, 1),
                    pos_hint={"right": 0.95},
                    halign="right",
                    valign="middle",
                    color=color,
                    outline_width=1*self.font_ratio,
                    outline_color=WHITE
                )
                score_label.bind(size=score_label.setter('text_size'))
                relative_layout.add_widget(score_label)

                scrollview_layout.add_widget(relative_layout)

            else:
                ### Three dots separation ###
                label = Label(
                    text=".\n.\n.",
                    font_name=self.font_name,
                    font_size=SUB_TEXT_FONT_SIZE * self.font_ratio,
                    size_hint=(1, None),
                    height=65*self.font_ratio,
                    halign="center",
                    valign="middle",
                    color=BLACK,
                    outline_width=1*self.font_ratio,
                    outline_color=WHITE,
                    line_height=0.5
                )
                label.bind(size=label.setter('text_size'))
                scrollview_layout.add_widget(label)

    def on_leave(self, *args):
        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        super().on_leave(*args)
