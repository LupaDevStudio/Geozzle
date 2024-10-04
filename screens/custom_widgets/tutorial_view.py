"""
Module to create a view for an interactive tutorial
"""

###########
# Imports #
###########

from copy import copy, deepcopy

from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    ColorProperty
)

#########
# Class #
#########


class TutorialView(ModalView):
    auto_dismiss = False
    background_color = ColorProperty([0.7, 0.7, 0.7, 0.1])

    def __init__(self, widget_to_show, **kwargs):
        super().__init__(**kwargs)
        copy_of_widget = copy(widget_to_show)
        copy_of_widget.parent = None
        release_function = copy(widget_to_show.on_release)

        def release_tuto_button(*args):
            self.dismiss()
            release_function()
            widget_to_show.on_release = release_function

        copy_of_widget.on_release = release_tuto_button
        self.add_widget(copy_of_widget)

        self.open()
