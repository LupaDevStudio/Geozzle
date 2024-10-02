from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import (
    BooleanProperty
)


class ImageButton(ButtonBehavior, Image):
    disable_button = BooleanProperty(False)
    def __init__(self, source="", fit_mode="cover", release_function=lambda: 1 + 1, **kwargs):
        super().__init__(**kwargs)
        self.release_function = release_function
        self.source = source
        self.fit_mode = fit_mode
        self.always_release = True

    def on_press(self):
        if not self.disable_button:
            self.opacity = 0.8

    def on_release(self):
        if not self.disable_button:
            if self.collide_point(self.last_touch.x, self.last_touch.y):
                self.release_function()
            self.opacity = 1
