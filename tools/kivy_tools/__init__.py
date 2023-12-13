"""
Package containing useful tools and shortcuts for kivy development.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.lang import Builder

### Package imports ###

from tools.kivy_tools.tools_kivy import MyScrollViewLayout
from tools.kivy_tools.screen import ImprovedScreen
from tools.kivy_tools.image_with_text import ImageWithText
from tools.kivy_tools.image_with_text_button import ImageWithTextButton
from tools.kivy_tools.image_button import ImageButton

###############
### Process ###
###############

PATH_KIVY_FOLDER = "tools/kivy_tools/"

### Kv files ###

# Build the kv file for the custom style
Builder.load_file(PATH_KIVY_FOLDER + "extended_style.kv", encoding="utf-8")

# Build the kv file for screen
Builder.load_file(PATH_KIVY_FOLDER + "screen.kv", encoding="utf-8")

# Build the kv file for image with text
Builder.load_file(PATH_KIVY_FOLDER + "image_with_text.kv", encoding="utf-8")

# Build the kv file for image with text and button
Builder.load_file(PATH_KIVY_FOLDER +
                  "image_with_text_button.kv", encoding="utf-8")
