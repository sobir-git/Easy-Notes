from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

SM = ScreenManager(transition=NoTransition())

from lockscreen import LOCKSCREEN
from editscreen import EDITSCREEN
from mainscreen import MAINSCREEN

SM.add_widget(LOCKSCREEN)
SM.add_widget(MAINSCREEN)
SM.add_widget(EDITSCREEN)
