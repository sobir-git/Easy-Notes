from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.clock import Clock
import math


class ImageButton(ButtonBehavior, Image):
    image_down = StringProperty()
    image_normal = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.on_state, 0)

    def on_state(self, *args):
        if self.state == 'down':
            self.source = self.image_down
        elif self.state == 'normal':
            self.source = self.image_normal


class PlusButton(ButtonBehavior, Image):
    def collide_point(self, x, y):
        return math.hypot(self.center_x - x, self.center_y - y) <=\
            self.width / 1.95


class SearchButton(ButtonBehavior, Image):
    pass

