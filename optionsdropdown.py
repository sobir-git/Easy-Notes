from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.dropdown import DropDown
from custombutton import ImageButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

Builder.load_string(
    """
#: import custombutton custombutton
#: import os os
<DropDown>:
    Button:
        text: "Delete note"
    Button:
        text: "Do smth"

<OptionsButton>:
    image_normal: os.path.join('images', 'options_button.png')
    image_down: os.path.join('images', 'options_button_down.png')
    size_hint: None, None
    size: (100, 50)
    # size_hint_x: None
    # width: self.height

<Button>:
    size_hint: None, None
    size: 100, 50

""")


class OptionsButton(ImageButton):
    pass


options_button = OptionsButton()
b = BoxLayout()
b.add_widget(options_button)
options_button.top = b.top

od = DropDown()

options_button.bind(on_release=od.open)


class ThisApp(App):
    def build(self):
        return b


ThisApp().run()
