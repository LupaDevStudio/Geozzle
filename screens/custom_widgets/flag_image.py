"""
Module to create a flag image.
"""

###############
### Imports ###
###############

### Kivy imports ###

from kivy.uix.image import Image
from kivy.properties import ColorProperty
from kivy.uix.widget import Widget

### Local imports ###

from tools.path import (
    PATH_IMAGES
)

#############
### Class ###
#############

from kivy.uix.scatter import Scatter
from kivy.app import App
from kivy.graphics.svg import Svg
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder


# Builder.load_string("""
# <SvgWidget>:
#     do_rotation: False
# <FloatLayout>:
#     canvas.before:
#         Color:
#             rgb: (1, 1, 1)
#         Rectangle:
#             pos: self.pos
#             size: self.size
# """)

class FlagImage(Scatter):
    def __init__(self, **kwargs):
        super(FlagImage, self).__init__(**kwargs)
        with self.canvas:
            svg = Svg(PATH_IMAGES + "test.svg")
        self.size = svg.width, svg.height


# class SvgApp(App):
#     def build(self):
#         self.root = FloatLayout()

#         filename = PATH_IMAGES + "test.svg"
#         svg = SvgWidget(filename, size_hint=(None, None), pos_hint={'center_x': 0.5, 'top': 1})
#         self.root.add_widget(svg)
#         svg.scale = 2

# class FlagImage(Widget):

#     primary_color = ColorProperty((0, 0, 0, 1))

#     def __init__(self, **kw):
#         super().__init__(**kw)
#         # self.source = PATH_IMAGES + "interrogation_mark.png"
