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
    ANDROID_MODE,
    IOS_MODE
)
from tools.constants import (
    FPS,
    MSAA_LEVEL
)
from tools.geozzle import (
    SHARED_DATA
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

    def propagate_background_on_other_screens(self):

        current_screen = self.get_screen(self.current)

        for screen_name in self.screen_names:
            screen = self.get_screen(screen_name)

            if screen_name in (self.current, "opening", "temp"):
                continue

            if not screen.is_loaded:
                screen.preload()

            if screen.opacity_state == "main":
                if (current_screen.opacity_state == "main" and not current_screen.is_transition) or (current_screen.opacity_state == "second" and current_screen.is_transition):
                    screen.set_back_image_path(
                        current_screen.back_image_path, "main")
                    screen.set_back_image_path(
                        current_screen.back_image_path, "second")
                else:
                    screen.set_back_image_path(
                        current_screen.second_back_image_path, "main")
                    screen.set_back_image_path(
                        current_screen.second_back_image_path, "second")
            else:
                if (current_screen.opacity_state == "main" and not current_screen.is_transition) or (current_screen.opacity_state == "second" and current_screen.is_transition):
                    screen.set_back_image_path(
                        current_screen.back_image_path, "main")
                    screen.set_back_image_path(
                        current_screen.back_image_path, "second")
                else:
                    screen.set_back_image_path(
                        current_screen.second_back_image_path, "main")
                    screen.set_back_image_path(
                        current_screen.second_back_image_path, "second")

    def change_background(self, *args, background_path=None):
        # Get current screen to change its background
        current_screen = self.get_screen(self.current)

        # Change the image of the background
        if current_screen.opacity_state == "main":
            if background_path is not None:
                image = background_path
            else:
                image = rd.choice(SHARED_DATA.list_unlocked_backgrounds)

            # Verify that the new image is not the same as the current one
            while image == current_screen.back_image_path and background_path is None:
                image = rd.choice(SHARED_DATA.list_unlocked_backgrounds)

            if image != current_screen.back_image_path:
                current_screen.set_back_image_path(
                    back_image_path=image,
                    mode="second"
                )
                change_image = True
            else:
                change_image = False

        else:
            if background_path is not None:
                image = background_path
            else:
                image = rd.choice(SHARED_DATA.list_unlocked_backgrounds)

            # Verify that the new image is not the same as the current one
            while image == current_screen.second_back_image_path and background_path is None:
                image = rd.choice(SHARED_DATA.list_unlocked_backgrounds)

            if image != current_screen.second_back_image_path:
                current_screen.set_back_image_path(
                    back_image_path=image,
                    mode="main"
                )
                change_image = True
            else:
                change_image = False

        if change_image:
            # Schedule the change of the opacity to have a smooth transition
            Clock.schedule_interval(
                current_screen.change_background_opacity, 1 / FPS)
            current_screen.is_transition = True

            # Start the color animation
            current_screen.animate_color_change()

            # Inform other screens of the change
            self.propagate_background_on_other_screens()


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
        if ANDROID_MODE:
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
    if not (ANDROID_MODE or IOS_MODE):
        Window.size = (405, 720)
        # For screenshots for App Store Iphone
        # Window.size = (461, 1000)
        # For screenshots for App Store Ipad
        # Window.size = (750, 1000)
        # For screenshots for Play Store
        # Window.size = (400, 720)
    main_app = MainApp()
    main_app.run()
