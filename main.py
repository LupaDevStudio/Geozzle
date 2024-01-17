"""
Main module of Geozzle.
"""

###############
### Imports ###
###############

### Python imports ###

import os
import random as rd

### Kivy imports ###

# Disable back arrow
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock

### Local imports ###

from tools.path import (
    PATH_IMAGES,
    PATH_BACKGROUNDS
)
from tools.constants import (
    MOBILE_MODE,
    FPS,
    MSAA_LEVEL
)
import screens.opening

###############
### General ###
###############


class WindowManager(ScreenManager):
    """
    Screen manager, which allows the navigation between the different menus.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()
        self.list_former_screens = []
        current_screen = Screen(name="temp")
        self.add_widget(current_screen)
        self.current = "temp"

    def set_right_background_with_previous(self):
        current_screen = self.get_screen(self.current)
        previous_screen = self.get_screen(current_screen.previous_screen_name)

        if current_screen.opacity_state == "main":
            if (previous_screen.opacity_state == "main" and not previous_screen.is_transition) or (
                    previous_screen.opacity_state == "second" and previous_screen.is_transition):
                current_screen.set_back_image_path(
                    previous_screen.back_image_path)
            else:
                current_screen.set_back_image_path(
                    previous_screen.second_back_image_path)
        else:
            if (previous_screen.opacity_state == "main" and not previous_screen.is_transition) or (
                    previous_screen.opacity_state == "second" and previous_screen.is_transition):
                current_screen.set_back_image_path(
                    previous_screen.back_image_path, "second")
            else:
                current_screen.set_back_image_path(
                    previous_screen.second_back_image_path, "second")

    def change_background(self, *args):
        # Get current screen to change its background
        current_screen = self.get_screen(self.current)

        # Change the image of the background
        if current_screen.opacity_state == "main":
            image = rd.choice(os.listdir(PATH_BACKGROUNDS +
                              current_screen.code_continent))

            # verify that the new image is not the same as the current one
            while image == current_screen.back_image_path.split("/")[-1]:
                image = rd.choice(os.listdir(
                    PATH_BACKGROUNDS + current_screen.code_continent))

            current_screen.set_back_image_path(
                back_image_path=PATH_BACKGROUNDS + current_screen.code_continent + "/" + image,
                mode="second"
            )

        else:
            image = rd.choice(os.listdir(PATH_BACKGROUNDS +
                              current_screen.code_continent))

            # verify that the new image is not the same as the current one
            while image == current_screen.second_back_image_path.split("/")[-1]:
                image = rd.choice(os.listdir(
                    PATH_BACKGROUNDS + current_screen.code_continent))

            current_screen.set_back_image_path(
                back_image_path=PATH_BACKGROUNDS + current_screen.code_continent + "/" + image,
                mode="main"
            )

        # Schedule the change of the opacity to have a smooth transition
        Clock.schedule_interval(
            current_screen.change_background_opacity, 1 / FPS)


class MainApp(App, Widget):
    """
    Main class of the application.
    """

    def build_config(self, config):
        """
        Build the config file for the application.

        It sets the FPS number and the antialiasing level.
        """
        config.setdefaults('graphics', {
            'maxfps': str(FPS),
            'multisamples': str(MSAA_LEVEL)
        })

    def build(self):
        """
        Build the application.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        Window.clearcolor = (0, 0, 0, 1)
        self.icon = PATH_IMAGES + "logo.png"

    def on_resume(self):
        current_screen_name = self.root_window.children[0].current
        self.root_window.children[0].get_screen(current_screen_name).refresh()
        return super().on_resume()

    def on_start(self):
        if MOBILE_MODE:
            Window.update_viewport()

        # Open the opening screen
        opening_screen = screens.opening.OpeningScreen(name="opening")
        self.root_window.children[0].add_widget(opening_screen)
        self.root_window.children[0].current = "opening"

        Clock.schedule_once(
            self.root_window.children[0].get_screen("opening").launch_thread)

        print("Main app started")

        return super().on_start()


# Run the application
if __name__ == "__main__":
    Window.size = (405, 720)
    MainApp().run()
