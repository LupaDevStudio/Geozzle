"""
Module to create the bottom bar with the buttons.
"""

###############
### Imports ###
###############

### Kivy imports ###
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ListProperty, StringProperty, ObjectProperty

### Local imports ###
from tools.kivy_tools import ImageButton

#############
### Class ###
#############


class BottomBar(RelativeLayout):
    background_color = (0, 0, 0, 0.5)
    separation_color = (1, 1, 1, 1)
    selected_color = (1, 0, 0, 1)
    separation_height = 3
    button_width = 0.15
    button_height = 0.7
    selected = StringProperty()
    selected_rect_pos = ObjectProperty((0, 0))
    selected_rect_size = ObjectProperty((0, 0))

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_kv_post(self, base_widget):
        if self.selected + "_button" in self.ids.keys():
            self.selected_rect_pos = self.ids[self.selected +
                                              "_button"].pos_hint
            self.selected_rect_size = \
                (self.ids[self.selected + "_button"].size_hint[0] * 1.2,
                 self.ids[self.selected + "_button"].size_hint[1] * 1.2)
        return super().on_kv_post(base_widget)
