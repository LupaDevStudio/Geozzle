"""
Module to create a spinner with a custom style
"""


###############
### Imports ###
###############

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.properties import (
    ColorProperty,
    NumericProperty
)

###############
### Classes ###
###############


class CustomSpinnerOption(ButtonBehavior, Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CustomDropDown(DropDown):
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown_cls = CustomDropDown
        self.option_cls = CustomSpinnerOption
