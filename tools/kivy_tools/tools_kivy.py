"""
Module for general Kivy widgets and functions.
"""

###############
### Imports ###
###############


### Kivy imports ###

from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.compat import string_types
from kivy.factory import Factory

### Python imports ###

from functools import partial

### Modules imports ###

my_language = {}
PATH_KIVY_FOLDER = "tools/kivy_tools/"

########################
### Global Variables ###
########################


### Kivy theme ###

size_popup = (int(Window.size[0] / 1.2), int(Window.size[1] / 2))
global_spacing = {
    "horizontal": Window.size[0] / 50,
    "vertical": Window.size[1] / 50
}
background_color = (70 / 255, 65 / 255, 62 / 255, 1)
color_label = (254 / 255, 195 / 255, 3 / 255, 1)
color_label_popup = (1, 1, 1, 1)
blue_color = (70 / 255, 130 / 255, 180 / 255, 1)
pink_color = (229 / 255, 19 / 255, 100 / 255, 1)
highlight_text_color = (229 / 255, 19 / 255, 100 / 255, 0.5)

scale_image = 3 * Window.size[1] / 2340


def get_window_ratio():
    """
    Return the ratio of the current window.
    """
    return Window.size[0] / Window.size[1]


#####################
### Popup windows ###
#####################


def blank_function(*args, **kwargs):
    """
    Function that does nothing
    """


class ImprovedPopupLayout(FloatLayout):
    """
    Class used to make the background of the popup with the pink line
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    pink_color = pink_color
    blue_color = blue_color
    size_popup = size_popup


class ImprovedPopup(Popup):
    """
    Class used to easily create popups
    """

    def __init__(self, title="Popup", size_hint=(None, None), auto_dismiss=False, add_content=[], size=size_popup, font="Roboto"):

        # Initialisation du layout contenant les objets du popup
        self.layout = ImprovedPopupLayout()
        # Initialisation du popup par héritage
        super().__init__(title=title, size_hint=size_hint,
                         auto_dismiss=auto_dismiss, content=self.layout, size=size, title_font=font)
        # Ajout du bouton de fermeture
        self.add_close_button()
        # Ajout des composants voulus
        correspondance_list = [
            ("label", self.add_label),
            ("text_input", self.add_text_input),
            ("spinner", self.add_spinner),
            ("progress_bar", self.add_progress_bar),
            ("button", self.add_button),
            ("widget", self.add_other_widget)
        ]
        for instruction in add_content:
            for i in range(len(correspondance_list)):
                if instruction[0] == correspondance_list[i][0]:
                    correspondance_list[i][1](**instruction[1])
        # Ouverture du popup
        self.open()

    def add_close_button(self):
        pos_hint = {"right": 1, "y": 1 + 8 / self.height}
        size = (dp(32), dp(32))
        size_hint = (None, None)
        close_button = Button(
            background_color=(0, 0, 0, 0),
            pos_hint=pos_hint,
            size_hint=size_hint,
            size=size
        )
        close_button.on_release = self.dismiss
        close_button_image = Image(
            source=PATH_KIVY_FOLDER + "images/close_button.png",
            pos_hint=pos_hint,
            size_hint=size_hint,
            size=size
        )
        self.layout.add_widget(close_button)
        self.layout.add_widget(close_button_image)

    def add_label(self, text="", size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "top": 0.9}, bool_text_size=False, **kwargs):
        label = Label(
            text=text,
            size_hint=size_hint,
            pos_hint=pos_hint,
            shorten=False,
            text_size=(
                int(size_hint[0] * Window.size[0] * 0.95), None),
            **kwargs)
        if bool_text_size:
            label.text_size = label.size
            label.halign = "left"
            label.valign = "center"
        else:
            label.halign = "center"
        self.layout.add_widget(label)
        return label

    def add_text_input(self, text="", pos_hint={"x": 0.1, "top": 0.7}, size_hint=(0.8, 0.2), multiline=False, **kwargs):
        text_input = TextInput(text=text,
                               size_hint=size_hint,
                               pos_hint=pos_hint,
                               selection_color=highlight_text_color,
                               multiline=multiline, **kwargs)
        self.layout.add_widget(text_input)

    def add_spinner(self, text="Spinner", values=["Spin 1", "Spin 2"], size_hint=(0.6, 0.2), pos_hint={"x": 0.2, "top": 0.7}, halign="center", **kwargs):
        spinner = Spinner(text=text,
                          values=values,
                          size_hint=size_hint,
                          pos_hint=pos_hint,
                          halign=halign, **kwargs)
        self.layout.add_widget(spinner)

    def add_progress_bar(self, max=100, pos_hint={"center_x": 0.5, "top": 0.85}, size_hint=(0.5, 0.25), **kwargs):
        progress_bar = ProgressBar(
            max=max,
            pos_hint=pos_hint,
            size_hint=size_hint,
            **kwargs)
        # Set progress_bar as property in order to change its value later on
        self.progress_bar = progress_bar
        self.layout.add_widget(progress_bar)
        return progress_bar

    def add_button(self, text="", disabled=False, size_hint=(0.8, 0.2), pos_hint={"x": 0.1, "top": 0.45}, halign="center", on_release=blank_function, **kwargs):
        button = FocusableButton(
            text=text,
            size_hint=size_hint,
            pos_hint=pos_hint,
            halign=halign,
            disabled=disabled,
            **kwargs)
        button.on_release = on_release
        self.layout.add_widget(button)
        return button

    def add_checkbox(self, text="", color_label=color_label_popup,
                     size_hint_cb=(0.05, 0.05), pos_hint={"x": 0.1, "y": 0},
                     group=None, size_hint_label=(0.05, 0.1),
                     function_cb=blank_function,
                     disabled=False, **kwargs):
        checkbox = LabelledCheckBox(
            text_label=text,
            color_label=color_label,
            size_hint_label=size_hint_label,
            size_hint_cb=size_hint_cb,
            pos_hint=pos_hint,
            group=group,
            function_cb=function_cb,
            disabled=disabled,
            **kwargs)
        self.layout.add_widget(checkbox)
        return checkbox

    def add_other_widget(self, widget_class, **kwargs):
        widget = widget_class(**kwargs)
        self.layout.add_widget(widget)
        return widget


# def create_standard_popup(title_popup, message, button_message=my_language.dict_buttons["close"]):
#     popup_content = [
#         ("label", {
#             "text": message,
#             "pos_hint": {"x": 0.1, "y": 0.6},
#             "size_hint": (0.8, 0.15)
#         })
#     ]
#     popup = ImprovedPopup(
#         title=title_popup,
#         add_content=popup_content)
#     button = popup.add_button(
#         text=button_message,
#         pos_hint={"x": 0.2, "y": 0.25},
#         size_hint=(0.6, 0.15)
#     )
#     button.on_release = popup.dismiss
#     button.focus = True


####################
### Scroll views ###
####################


class MyScrollViewLayout(GridLayout):
    """
    Class corresponding to the layout inside the scroll view
    """

    def __init__(self, **kwargs):
        super(MyScrollViewLayout, self).__init__(**kwargs)
        self.size_hint_y = (None)
        self.bind(minimum_height=self.setter('height'))

    def reset_screen(self):
        list_widgets = self.children[:]
        for element in list_widgets:
            self.remove_widget(element)


#######################
### Focusable items ###
#######################


class FocusableSpinner(FocusBehavior, Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_is_open(self, instance, value):
        if self.is_open:
            self._dropdown.clear_widgets()
            for value in self.values:
                btn = FocusableButton(
                    text=value,
                    size_hint_y=None,
                    height=self.height,
                    font_name=self.font_name,
                    font_size=self.font_size
                )
                btn.on_release = partial(self.on_button_press, btn)
                self._dropdown.add_widget(btn)
        return super().on_is_open(instance, value)

    def on_button_press(self, button):
        self._dropdown.select(button.text)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        key = keycode[-1]
        if key in ("spacebar", "enter"):
            self.is_open = not self.is_open
            if self.is_open:
                self._dropdown.children[0].children[-1].focus = True

        return super(FocusableSpinner, self).keyboard_on_key_down(window, keycode, text, modifiers)


class ToolTip(Label):
    pass


class FocusableButton(FocusBehavior, Button):
    tooltip_text = StringProperty('')
    tooltip_cls = ObjectProperty(ToolTip)

    def __init__(self, scroll_to=False, **kwargs):
        self._tooltip = None
        self.scroll_to = scroll_to
        super().__init__(**kwargs)
        fbind = self.fbind
        fbind('tooltip_cls', self._build_tooltip)
        fbind('tooltip_text', self._update_tooltip)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self._build_tooltip()

    def _build_tooltip(self, *largs):
        if self._tooltip:
            self._tooltip = None
        cls = self.tooltip_cls
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        self._tooltip = cls()
        self._update_tooltip()

    def _update_tooltip(self, *largs):
        self._tooltip.text = self.tooltip_text

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        key = keycode[-1]
        if key in ("spacebar", "enter"):
            self.on_release()

        return super(FocusableButton, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def on_mouse_pos(self, *args):
        if self.tooltip_text != "":
            if not self.get_root_window():
                return
            pos = args[1]
            self._tooltip.pos = pos
            # cancel scheduled event since I moved the cursor
            Clock.unschedule(self.display_tooltip)
            self.close_tooltip()  # close if it's opened
            if self.collide_point(*self.to_widget(*pos)):
                Clock.schedule_once(self.display_tooltip, 1)

    def close_tooltip(self, *args):
        Window.remove_widget(self._tooltip)

    def display_tooltip(self, *args):
        Window.add_widget(self._tooltip)

    def _on_focus(self, instance, value, *largs):
        if self.scroll_to:
            if (self.parent.number_lines + 1) * self.parent.size_line > self.parent.parent.height:
                self.parent.parent.scroll_to(self)
        return super()._on_focus(instance, value, *largs)


class FocusableCheckBox(FocusBehavior, CheckBox):
    def __init__(self, scroll_to=False, **kwargs):
        self.scroll_to = scroll_to
        super().__init__(**kwargs)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        key = keycode[-1]
        if key in ("spacebar", "enter"):
            self.active = not self.active
        return super(FocusableCheckBox, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def _on_focus(self, instance, value, *largs):
        if self.scroll_to:
            if (self.parent.number_lines + 1) * self.parent.size_line > self.parent.parent.height:
                self.parent.parent.scroll_to(self)
        return super()._on_focus(instance, value, *largs)


class LabelledCheckBox(FloatLayout):
    def __init__(self, text_label="",
                 size_hint_label=(0.05, 0.1),
                 color_label=(0, 0, 0, 1),
                 pos_hint={"x": 0, "y": 0},
                 size_hint_cb=(0.05, 0.05),
                 function_cb=blank_function,
                 disabled=False,
                 group=None, **kwargs):
        self.text_label = text_label
        self.size_hint_label = size_hint_label
        self.color_label = color_label
        self.pos_hint = pos_hint
        self.size_hint_cb = size_hint_cb
        self.function_cb = function_cb
        self.group = group
        self.disabled_cb = disabled
        super().__init__(**kwargs)


class FocusableTextInput(TextInput):
    def __init__(self, scroll_to=False, **kwargs):
        self.scroll_to = scroll_to
        self.write_tab = False
        super().__init__(**kwargs)
        self.last_value = self.text

    def _on_focus(self, instance, value, *largs):
        if self.scroll_to:
            if (self.parent.number_lines + 1) * self.parent.size_line > self.parent.parent.height:
                self.parent.parent.scroll_to(self)
        return super()._on_focus(instance, value, *largs)
