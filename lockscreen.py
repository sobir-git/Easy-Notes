from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from database import DATABASE

Builder.load_file("lockscreen.kv")


class LockScreen(Screen):
    def check_password(self, password):
        """ If password is correct switch to main screen. """
        if password == 'git':
            SM.current = 'mainscreen'


LOCKSCREEN = LockScreen(name='lockscreen')

from screenmanager import SM
