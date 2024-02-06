"""
Module to create a spinner with a custom style
"""


###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.properties import (
    ColorProperty,
    NumericProperty
)

### Local imports ###

from tools import sound_mixer


###############
### Classes ###
###############


class CustomSpinnerOption(ButtonBehavior, Label):

    font_ratio = NumericProperty(1)
    select_color = ColorProperty((0.5, 0.5, 0.5, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.always_release = True

    def on_press(self):
        self.color = self.select_color
        sound_mixer.play("click")
        return super().on_press()

    def on_release(self):
        self.color = self.parent.parent.text_color
        return super().on_release()


class CustomDropDown(DropDown):

    font_ratio = NumericProperty(1)
    border_color = ColorProperty((0, 0, 0, 1))
    background_color = ColorProperty((1, 1, 1, 1))
    text_color = ColorProperty((0, 0, 0, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CustomSpinner(Spinner):

    font_ratio = NumericProperty(1)
    border_color = ColorProperty((0, 0, 0, 1))
    background_color = ColorProperty((1, 1, 1, 1))
    text_color = ColorProperty((0, 0, 0, 1))
    select_color = ColorProperty((0.5, 0.5, 0.5, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown_cls = CustomDropDown
        self.option_cls = CustomSpinnerOption

    def on_press(self):
        sound_mixer.play("click")
        return super().on_press()
