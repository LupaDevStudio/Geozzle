"""
Module to create the home screen.
"""

###############
### Imports ###
###############

### Python imports ###

import os
import random as rd
from functools import partial

### Kivy imports ###

from kivy.properties import (
    StringProperty
)
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_CONTINENTS_IMAGES
)
from screens.custom_widgets import (
    GeozzleScreen,
    CircleProgressBar,
    MyScrollViewLayout,
    StatsLayout
)
from tools.constants import (
    LIST_CONTINENTS,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP,
    DICT_CONTINENTS_PRIMARY_COLOR,
    DICT_CONTINENT_SECOND_COLOR,
    HIGHSCORE_FONT_SIZE,
    SUBTITLE_OUTLINE_WIDTH,
    WHITE,
    TIME_CHANGE_BACKGROUND
)
from tools.geozzle import (
    USER_DATA,
    TEXT,
    SHARED_DATA
)

#############
### Class ###
#############


class StatsScreen(GeozzleScreen):

    highscore_label = StringProperty()
    buy_background_label = StringProperty()

    dict_type_screen = {
        SCREEN_TITLE: {
            "title": "stats"
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

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def on_enter(self, *args):
        super().on_enter(*args)

        # Schedule the change of background
        if self.previous_screen_name in ["stats_continent"]:
            Clock.schedule_interval(
                self.manager.change_background, TIME_CHANGE_BACKGROUND)

    def fill_scrollview(self):
        scrollview_layout: MyScrollViewLayout = self.ids.scrollview_layout

        for code_continent in LIST_CONTINENTS:
            # Label with the name of the continent
            label = Label(
                text=TEXT.home[code_continent],
                font_name=self.font_name,
                font_size=HIGHSCORE_FONT_SIZE * self.font_ratio,
                size_hint=(1, None),
                height=40 * self.font_ratio,
                halign="center",
                valign="middle",
                color=DICT_CONTINENTS_PRIMARY_COLOR[code_continent],
                outline_width=max(SUBTITLE_OUTLINE_WIDTH * self.font_ratio, 1),
                outline_color=WHITE
            )
            label.bind(size=label.setter('text_size'))
            scrollview_layout.add_widget(label)

            # Relative layout with the counter and the stats background
            height_layout = 150 * self.font_ratio
            layout = RelativeLayout(
                size_hint=(1, None),
                height=height_layout
            )

            # Progress circle
            progress_circle = CircleProgressBar(
                source=PATH_CONTINENTS_IMAGES + code_continent + ".jpg",
                size_hint=(0.3, None),
                pos_hint={"center_y": 0.5},
                font_ratio=self.font_ratio,
                circle_color=DICT_CONTINENTS_PRIMARY_COLOR[code_continent],
                progress=USER_DATA.get_continent_progress(
                    code_continent=code_continent)
            )
            progress_circle.bind(width=progress_circle.setter("height"))
            layout.add_widget(progress_circle)

            # Stats layout
            number_countries = USER_DATA.get_nb_countries(
                code_continent=code_continent)
            text = ""
            for i in range(1, 4):
                number_countries_stars = USER_DATA.get_nb_countries_with_stars(
                    code_continent=code_continent,
                    target_nb_stars=i)
                text += f"{number_countries_stars} / {number_countries}\n"
            text = text[:-1]
            stats_layout = StatsLayout(
                font_ratio=self.font_ratio,
                size_hint=(0.6, None),
                height=height_layout * 0.9,
                pos_hint={"center_y": 0.5, "x": 0.4},
                text=text,
                text_button=TEXT.stats["details"],
                color_label=DICT_CONTINENTS_PRIMARY_COLOR[code_continent],
                background_button_color=DICT_CONTINENT_SECOND_COLOR[code_continent],
                release_function=partial(
                    self.open_continent_details, code_continent)
            )
            layout.add_widget(stats_layout)

            scrollview_layout.add_widget(layout)

    def open_continent_details(self, code_continent: str):
        self.manager.get_screen(
            "stats_continent").code_continent = code_continent
        # Unschedule the clock updates
        Clock.unschedule(self.manager.change_background,
                         TIME_CHANGE_BACKGROUND)
        Clock.schedule_once(self.manager.get_screen(
            "stats_continent").change_background_continent)
        self.manager.current = "stats_continent"

    def on_leave(self, *args):
        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        super().on_leave(*args)
