from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


class ImageButton(ButtonBehavior, Image):
    def __init__(self, source="", release_function=lambda: 1 + 1, **kwargs):
        super().__init__(**kwargs)
        self.release_function = release_function
        self.source = source
        self.fit_mode = "contain"
        self.always_release = True

    def on_press(self):
        self.opacity = 0.8

    def on_release(self):
        self.release_function()
        self.opacity = 1
