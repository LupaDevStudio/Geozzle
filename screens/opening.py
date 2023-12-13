"""
Module for the opening screen.
"""

###############
### Imports ###
###############

import os
from threading import Thread
from tools.kivy_tools import ImprovedScreen
from tools.path import (
    PATH_IMAGES
)
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label


class OpeningScreen(ImprovedScreen):
    """
    Screen of Opening.
    """

    def __init__(self, **kw):
        super().__init__(
            back_image_path=PATH_IMAGES + "opening.jpg",
            **kw)
        self.opacity_state = -1
        self.opacity_rate = 0.03
        self.label = Label(text="", pos_hint={
            "bottom": 1, "left": 1})
        self.add_widget(self.label)

    def update(self, *args):
        self.label.opacity += self.opacity_state * self.opacity_rate
        if self.label.opacity < 0 or self.label.opacity > 1:
            self.opacity_state = -self.opacity_state

    def on_enter(self, *args):
        print("enter opening screen")
        # Schedule the update for the text opacity effect
        Clock.schedule_interval(self.update, 1 / 60)

        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        # Unschedule the clock update
        Clock.unschedule(self.update, 1 / 60)

        return super().on_leave(*args)

    def launch_thread(self, *_):
        thread = Thread(target=self.load_kv_files)
        thread.start()

    def load_kv_files(self, *_):
        from screens import (
            HomeScreen)

        screen_files = [file for file in os.listdir(
            "screens") if file.endswith(".kv")]
        for file in screen_files:
            Builder.load_file(f"screens/{file}", encoding="utf-8")
        widget_files = [file for file in os.listdir(
            "screens/custom_widgets") if file.endswith(".kv")]
        for file in widget_files:
            Builder.load_file(
                f"screens/custom_widgets/{file}", encoding="utf-8")

        self.HomeScreen = HomeScreen

        Clock.schedule_once(self.load_other_screens)

    def switch_to_menu(self, *args):
        self.manager.current = "home"

    def load_other_screens(self, *args):

        ### Load the kv files of the screens ###
        home_screen = self.HomeScreen(name="home")
        self.manager.add_widget(home_screen)
        # game_screen = self.GameScreen(name="game")
        # self.manager.add_widget(game_screen)
        # settings_screen = self.SettingsScreen(name="settings")
        # self.manager.add_widget(settings_screen)
        # game_over_screen = self.GameOverScreen(name="game_over")
        # self.manager.add_widget(game_over_screen)
        # achievements_screen = self.AchievementsScreen(name="achievements")
        # self.manager.add_widget(achievements_screen)
        # tutorial_screen = self.TutorialScreen(name="tutorial")
        # self.manager.add_widget(tutorial_screen)
        # help_screen = self.HelpScreen(name="help")
        # self.manager.add_widget(help_screen)
        # Preload screens
        # Clock.schedule_once(self.manager.get_screen("game").preload)
        # Clock.schedule_once(self.manager.get_screen("game_over").preload)
        # self.manager.current = "menu"
        Clock.schedule_once(self.switch_to_menu)
