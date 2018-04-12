from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from database import DATABASE

Builder.load_file("mainscreen.kv")


class MainScreen(Screen):
    # when new note is requested
    def on_new_note(self, *args):
        # switch to edit screen
        SM.current = 'editscreen'
        # create a new note on edit screen
        editscreen = self.parent.get_screen("editscreen")
        editscreen.new_note()


class RV(RecycleView):
    """ Recycle View for notes. """

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self._all_data = [{'note': note}
                          for key, note in DATABASE.sorted_by_key()]
        self.data = self._all_data

    def search(self, s):
        """ Search for string s in all data and filter it"""
        if s.isspace():
            self.data = self._all_data
            return
        s = s.strip().lower()
        _data = []
        for key, note in DATABASE.sorted_by_key():
            if note.text.lower().find(s) != -1:
                _data.append({'note': note})
        self.data = _data

    def add_new_note(self, note):
        self.data.insert(0, {'note': note})


class NotePreview(ButtonBehavior, BoxLayout):
    """ A class for note preview on main screen.
    Inherits Button Behaviours (on_release)
    """
    DATE_VIEW_FORMAT = "%B %d, %Y\n%a, %H:%M"

    def on_release(self):
        # switch to edit screen
        SM.current = "editscreen"
        # send self.note to modify_note for editing
        SM.get_screen('editscreen').modify_note(self.note)


MAINSCREEN = MainScreen(name='mainscreen')
MAINSCREEN.RV = RV()


from screenmanager import SM
from editscreen import EDITSCREEN
from lockscreen import LOCKSCREEN
