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
from kivy.uix.label import Label
from kivy.uix.image import Image

### Local imports ###

from tools.path import (
    PATH_TEXT_FONT,
    PATH_BACKGROUNDS
)
from screens.custom_widgets import (
    GeozzleScreen,
    ImagePopup,
    MessagePopup,
    CustomScrollview,
    MyScrollViewLayout,
    MyScrollViewVerticalLayout
)
from tools.constants import (
    PRICE_BACKGROUND,
    SCREEN_TITLE,
    SCREEN_ICON_LEFT_UP,
    DICT_CONTINENTS_PRIMARY_COLOR,
    DICT_CONTINENT_SECOND_COLOR,
    SUB_TEXT_FONT_SIZE,
    SUBTITLE_OUTLINE_WIDTH,
    WHITE,
    BLACK,
    GRAY
)
from tools.kivy_tools import (
    ImageButton
)
from tools.geozzle import (
    USER_DATA,
    TEXT,
    SHARED_DATA
)

#############
### Class ###
#############


class GalleryScreen(GeozzleScreen):

    points_label = StringProperty()
    buy_background_label = StringProperty()

    dict_type_screen = {
        SCREEN_TITLE: {
            "title": "gallery"
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
        self.points_label = TEXT.gallery["points"].replace(
            "[POINTS]", str(USER_DATA.points))
        self.buy_background_label = TEXT.gallery["buy_background"].replace(
            "[POINTS]", str(PRICE_BACKGROUND))

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.fill_scrollview()

    def buy_background(self):
        # The user has enough points to buy the background
        if USER_DATA.can_buy_background:
            dict_details = USER_DATA.buy_new_background()
            self.reload_language()
            code_continent = dict_details["code_continent"]
            full_path = dict_details["full_path"]
            is_new = dict_details["is_new"]
            if is_new:
                title = TEXT.gallery["new_background"]
                self.rebuild_scrollview()
            else:
                title = TEXT.gallery["already_bought_background"]

            # Open a popup showing the new bought background
            popup = ImagePopup(
                font_ratio=self.font_ratio,
                primary_color=DICT_CONTINENTS_PRIMARY_COLOR[code_continent],
                secondary_color=DICT_CONTINENT_SECOND_COLOR[code_continent],
                title=title,
                image_source=full_path,
                release_function=partial(self.manager.change_background, background_path=full_path),
                ok_button_label=TEXT.popup["close"]
            )
            popup.open()
        
        # Error popup when the user doesn't have enough points
        else:
            popup = MessagePopup(
                font_ratio=self.font_ratio,
                primary_color=BLACK,
                secondary_color=GRAY,
                title=TEXT.popup["buy_background_impossible_title"],
                center_label_text=TEXT.popup["buy_background_impossible_text"].replace("[NB_POINTS]", str(PRICE_BACKGROUND)),
                ok_button_label=TEXT.popup["close"]
            )
            popup.open()

    def fill_scrollview(self):
        scrollview_layout: MyScrollViewLayout = self.ids.scrollview_layout

        for code_continent in list(DICT_CONTINENTS_PRIMARY_COLOR.keys()):
            list_backgrounds = [background for background in os.listdir(PATH_BACKGROUNDS + code_continent) if background in USER_DATA.unlocked_backgrounds]
            number_backgrounds = len(os.listdir(PATH_BACKGROUNDS + code_continent))
            # Label with the name of the continent
            label = Label(
                text=TEXT.home[code_continent] + f" - {len(list_backgrounds)}/{number_backgrounds}",
                font_name=self.font_name,
                font_size=SUB_TEXT_FONT_SIZE*self.font_ratio,
                size_hint=(1, None),
                height=40*self.font_ratio,
                halign="left",
                valign="middle",
                color=DICT_CONTINENTS_PRIMARY_COLOR[code_continent],
                outline_width=max(SUBTITLE_OUTLINE_WIDTH*self.font_ratio, 1),
                outline_color=WHITE
            )
            label.bind(size=label.setter('text_size'))
            scrollview_layout.add_widget(label)

            # Vertical scrollview with background
            sv_height = 150*self.font_ratio
            custom_sv = CustomScrollview(
                font_ratio=self.font_ratio,
                background_mode=True,
                bar_width=5*self.font_ratio,
                bar_color=DICT_CONTINENT_SECOND_COLOR[code_continent],
                bar_inactive_color=DICT_CONTINENTS_PRIMARY_COLOR[code_continent],
                size_hint=(1, None),
                height=sv_height,
                bar_margin=8*self.font_ratio,
                do_scroll_y=False,
                do_scroll_x=True
            )
            vertical_layout = MyScrollViewVerticalLayout(
                rows=1,
                spacing=15*self.font_ratio,
                padding=15*self.font_ratio
            )

            # All the backgrounds
            for background in os.listdir(PATH_BACKGROUNDS + code_continent):
                full_path = PATH_BACKGROUNDS + code_continent + "/" + background
                if not full_path in SHARED_DATA.list_unlocked_backgrounds:
                    full_path = PATH_BACKGROUNDS + "unknown_background.jpg"
                    release_function = lambda: 1 + 1
                    disable_button = True
                else:
                    release_function = partial(self.manager.change_background, background_path=full_path)
                    disable_button = False
                image = ImageButton(
                    source=full_path,
                    size_hint=(None, None),
                    height=sv_height-15*self.font_ratio*2-8*self.font_ratio,
                    width=80*self.font_ratio,
                    pos_hint={"center_y": 0.5},
                    fit_mode="cover",
                    release_function=release_function,
                    disable_button=disable_button
                )
                if not full_path in SHARED_DATA.list_unlocked_backgrounds:
                    image.color = DICT_CONTINENT_SECOND_COLOR[code_continent]
                vertical_layout.add_widget(image)

            custom_sv.add_widget(vertical_layout)
            scrollview_layout.add_widget(custom_sv)

    def rebuild_scrollview(self):
        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        # Refill the scrollview
        self.fill_scrollview()

    def on_leave(self, *args):
        # Reset scrollview
        self.ids.scrollview_layout.reset_scrollview()
        super().on_leave(*args)
