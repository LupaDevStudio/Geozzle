"""
Module to create a custom scrollview with appropriate colors and size.
"""

##############
### Import ###
##############

### Kivy imports ###

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import (
    NumericProperty,
    BooleanProperty
)

#############
### Class ###
#############


class MyScrollViewLayout(GridLayout):
    """
    Class corresponding to the layout inside the scroll view
    """

    def __init__(self, **kwargs):
        super(MyScrollViewLayout, self).__init__(**kwargs)
        self.size_hint_y = (None)
        self.bind(minimum_height=self.setter('height'))

    def refill(self):
        self.setter("height")

    def reset_scrollview(self):
        list_widgets = self.children[:]
        for element in list_widgets:
            self.remove_widget(element)


class MyScrollViewVerticalLayout(GridLayout):
    """
    Class corresponding to the layout inside the scroll view
    """

    def __init__(self, **kwargs):
        super(MyScrollViewVerticalLayout, self).__init__(**kwargs)
        self.size_hint_x = (None)
        self.bind(minimum_width=self.setter('width'))

    def refill(self):
        self.setter("width")

    def reset_scrollview(self):
        list_widgets = self.children[:]
        for element in list_widgets:
            self.remove_widget(element)


class CustomScrollview(ScrollView):

    background_mode = BooleanProperty(False)
    font_ratio = NumericProperty(1)

    def on_scroll_move(self, touch):
        res = super().on_scroll_move(touch)
        if self.do_scroll_x and not self.do_scroll_y:
            touch.ud['sv.handled']['y'] = False
            res = False
        return res

    def on_scroll_stop(self, touch, check_children=True):
        if self.do_scroll_x and not self.do_scroll_y:
            super().on_scroll_stop(touch, check_children=False)
        else:
            super().on_scroll_stop(touch, check_children)
