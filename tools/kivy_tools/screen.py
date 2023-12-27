"""
Module to create an improved kivy screen with background and font support.
"""

###############
### Imports ###
###############

### Python imports ###

from copy import copy

### Kivy imports ###

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ObjectProperty
)

### Local imports ###

from tools.basic_tools import get_image_size
from tools.constants import (
    MOBILE_MODE,
    FPS,
    RATE_CHANGE_OPACITY
)

###############
### Classes ###
###############


class ImprovedScreen(Screen):
    """
    Improved Screen class based on the kivy one.
    """

    # Create the back image properties
    back_image_width = NumericProperty(Window.size[0])
    back_image_height = NumericProperty(Window.size[1])
    back_image_disabled = BooleanProperty(False)
    back_image_path = ObjectProperty("")
    second_back_image_path = ObjectProperty("")
    opacity_state = "main"

    # Create the font_name properties
    font_ratio = NumericProperty(1)
    font_name = StringProperty("Roboto")
    font_size_expand = 1

    def __init__(self, font_name="Roboto", back_image_path=None, second_back_image_path=None, **kw):

        # Create a dictionnary to store the positions of hidden widgets
        self.temp_pos = {}

        # Boolean to indicate whether the screen is loaded or no
        self.is_loaded = False

        # Set the font
        self.font_name = font_name

        # Store the back image path
        self.sto_back_image_path = back_image_path
        self.sto_second_back_image_path = second_back_image_path

        # Define all variables
        self.back_image_disabled = False
        self.back_image_opacity = 1
        self.second_back_image_opacity = 0
        self.back_image_ratio = 1

        # Init the kv screen
        super().__init__(**kw)

    def preload(self, *args):
        """
        Load all the assets of the screen.

        This is done here to be easily controlled and avoid computations on the app start.
        """

        # Indicate that the screen is loaded
        self.is_loaded = True

        # Set the background image
        if self.sto_back_image_path is not None:
            self.set_back_image_path(self.sto_back_image_path)
            self.back_image_opacity = 1
            self.back_image_disabled = False
        else:
            self.back_image_path = ""
            self.back_image_opacity = 0
            self.back_image_disabled = True

        # Set the second background image
        if self.sto_second_back_image_path is not None:
            self.second_back_image_path = self.sto_second_back_image_path
            self.second_back_image_opacity = 0
        else:
            self.second_back_image_path = ""
            self.second_back_image_opacity = 0

    def set_back_image_path(self, back_image_path):
        """
        Set a background image for the screen using a path.
        """

        # Set the source of the background image
        self.back_image_path = back_image_path

        # Compute the ratio to use for size computations
        width, height = get_image_size(back_image_path)
        self.back_image_ratio = width / height

        # Update the size of the background image
        self.update_back_image_size()

    def set_back_image_texture(self, back_image_texture):
        """
        Set a background image for the screen using a texture.
        """

        # Set the source of the background image
        self.ids["back_image"].texture = back_image_texture

        # Compute the ratio to use for size computations
        width, height = back_image_texture.size
        self.back_image_ratio = width / height

        # Update the size of the background image
        self.update_back_image_size()

    def update_back_image_size(self):
        """
        Update the size of the background image
        """
        window_ratio = Window.size[0] / Window.size[1]
        if window_ratio > self.back_image_ratio:
            self.back_image_width = Window.size[0]
            self.back_image_height = Window.size[0] / self.back_image_ratio
        else:
            self.back_image_width = Window.size[1] * self.back_image_ratio
            self.back_image_height = Window.size[1]

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        # Load the assets if it has not been done before
        if not self.is_loaded:
            self.preload()

        self.update_font_ratio()

        # Update the back image size
        self.update_back_image_size()

    def on_enter(self, *args):
        """
        Initialize the screen when it is opened.
        """

        # Bind to update attributes when the size of the window is changed
        Window.bind(on_resize=self.on_resize)

        # Add the screen name to the list of former screens
        self.manager.list_former_screens.append(self.name)

        # Update the back image size
        self.update_back_image_size()

        return super().on_enter(*args)

    def on_leave(self, *args):
        """
        Close when leaving the screen.
        """

        # Unbind the resize update
        Window.unbind(on_resize=self.on_resize)

        # Set the correct opacities for the background images
        if self.opacity_state == "main":
            self.ids.back_image.opacity = 1
            self.ids.second_back_image.opacity = 0
        elif self.opacity_state == "second":
            self.ids.back_image.opacity = 0
            self.ids.second_back_image.opacity = 1

        return super().on_leave(*args)

    def on_resize(self, *args):
        """
        Update attributes when the window size changes
        """
        self.update_back_image_size()
        self.update_font_ratio()

    def update_font_ratio(self):
        """
        Update the font_name ratio to use on the screen to keep letter size constant with Window size changes.
        """
        if MOBILE_MODE:
            self.font_ratio = Window.size[1] / \
                600 + (Window.size[0] / Window.size[1] - 1) * 0.5
        else:
            self.font_ratio = Window.size[1] / \
                600 + (Window.size[0] / Window.size[1] - 1) * 0.5

    def disable_widget(self, widget_id: str):
        """
        Disable the given widget.
        """
        widget = self.ids[widget_id]
        if not widget.disabled:
            widget.opacity = 0
            self.temp_pos[widget_id] = copy(widget.pos_hint)
            widget.pos_hint = {"x": 1, "y": 1}
            widget.disabled = True

    def enable_widget(self, widget_id: str):
        """
        Enable the given widget.
        """
        widget = self.ids[widget_id]
        widget.opacity = 1
        widget.disabled = False
        widget.pos_hint = self.temp_pos[widget_id]

    def refresh(self):
        self.label_widget = Label(text=" ", pos_hint={"x": 1, "y": 1})
        self.add_widget(self.label_widget)
        Clock.schedule_once(self.post_refresh)

    def post_refresh(self, *args):
        self.remove_widget(self.label_widget)

    def change_background_opacity(self, *args):
        """
        Change the opacity of both background images to change smoothly the background.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        """

        # If we have to display the second background image
        if self.opacity_state == "main":
            if self.ids.back_image.opacity >= 0:
                self.ids.back_image.opacity -= RATE_CHANGE_OPACITY
                self.ids.second_back_image.opacity += RATE_CHANGE_OPACITY
            else:
                Clock.unschedule(self.change_background_opacity, 1/FPS)
                self.opacity_state = "second"

        # If we have to display the background image
        elif self.opacity_state == "second":
            if self.ids.second_back_image.opacity >= 0:
                self.ids.back_image.opacity += RATE_CHANGE_OPACITY
                self.ids.second_back_image.opacity -= RATE_CHANGE_OPACITY
            else:
                Clock.unschedule(self.change_background_opacity, 1/FPS)
                self.opacity_state = "main"
