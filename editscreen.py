from kivy.uix.dropdown import DropDown
from kivy.properties import OptionProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from database import DATABASE

Builder.load_file("editscreen.kv")


class EditScreen(Screen):
    mode = OptionProperty("None", options=['new_note', 'modify_note'])
    options_dropdown = ObjectProperty()
    options_button = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def new_note(self):
        self.mode = 'new_note'
        self.note = Note(text='')

    def modify_note(self, note):
        # take the note for editing
        self.note = note
        self.mode = 'modify_note'

    def delete_note(self):
        popup_button = Button(text="Delete it!", size_hint_y=None, height=50)
        delpopup = Popup(content=popup_button,
                         title="Confirm note deletion", size_hint=(0.8, 0.5))
        popup_button.bind(on_release=delpopup.dismiss)
        popup_button.bind(on_release=self._delete_note)
        delpopup.open()

    def _delete_note(self, *args):
        # delete the current note
        if self.mode == 'modify_note':
            DATABASE.delete_note(self.note)
            SM.get_screen('mainscreen').rv.data.remove({'note': self.note})

        SM.current = 'mainscreen'

    def save_and_exit(self, *args):
        '''Save the note and exit this screen'''

        # if a new note
        if self.mode == 'new_note':
            # set note text
            self.note.set_text(self.note_input.text)
            # add this note to mainscreen notelist
            MAINSCREEN.rv.data.insert(0, {'note': self.note})
            # save it do database
            DATABASE.add_note(self.note)

        # if modify mode then save the changes
        elif self.mode == 'modify_note':
            self.note.modify_text(self.note_input.text)
            # update database
            DATABASE.update_note(self.note)

        SM.current = 'mainscreen'

    def cancel(self):
        # go to main screen without saving
        SM.current = 'mainscreen'


class OptionsDropDown(DropDown):
    def on_select(self, s):
        if s == 'save':
            EDITSCREEN.save_and_exit()
        elif s == 'delete':
            EDITSCREEN.delete_note()


EDITSCREEN = EditScreen(name='editscreen')
_options_dropdown = OptionsDropDown()
# _options_dropdown.save_btn.bind(on_release=_options_dropdown.select('save'))
# _options_dropdown.delete_btn.bind(on_release=_options_dropdown.select('delete'))

EDITSCREEN.options_button.bind(on_release=_options_dropdown.open)

from screenmanager import SM
from mainscreen import MAINSCREEN
from lockscreen import LOCKSCREEN
