from datetime import datetime
from kivy.storage.jsonstore import JsonStore
import operator
import os

class Note:
    """Class for note

    Attributes:
        text: Note text
        date_created: a datetime object
                      date in which note created
        date_modified: a datetime object or None
                       last date in which note is modified
                       defaults to None

    Methods:
        modify_text(self, new_text):
            replace current text with new_text and record modification date
    """

    def __init__(self, text='', date_created=None, date_modified=None):
        self._text = text
        self.date_modified = date_modified
        self._date_created = date_created if date_created else datetime.now()

    @property
    def date_created(self):
        return self._date_created

    @property
    def text(self):
        return self._text

    def modify_text(self, new_text):
        '''Modify the text of note to new_text
        '''
        self._text = new_text
        self.date_modified = datetime.now()

    def set_text(self, new_text):
        """ Set text of note, modify date will not be changed."""
        self._text = new_text


    def __str__(self):
        s =  "=================================================\n"
        s += "Note:\n"
        s += "Date created: {}\n".format(self.date_created)
        s += "Date modified: {}\n".format(self.date_modified
                                          if self.date_modified else "Not yet")
        s += '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' + self.text + '\n'
        s += '________________________________________________'
        return s


class NotesDB:
    """ A class for notes database.
    """
    # date and time string format to save and read datetime in json storage
    DATE_STR_FORMAT = "%Y-%m-%d-%H-%M-%S"

    def __init__(self, storage_file):
        """ initialize with storage and load all notes.
        storage_file: *.json filename"""

        all_notes = dict()
        keys = dict()
        if not os.path.exists(storage_file):
            # create and prepare general_info for a new storage
            storage = JsonStore(storage_file, indent=True)
            storage.put("general_info", last_id=0)
        else:
            storage = JsonStore(storage_file, indent=True)

            # load all notes in storage to a dict[key] = note
            for key in storage:
                if key == "general_info":
                    continue
                note = self.note_from_dict(storage[key])
                all_notes[key] = note
                keys[note] = key

        self._keys = keys
        self._storage = storage
        self.all_notes = all_notes

    def get_id(self):
        """ Return a new (key) id."""
        gd = self._storage['general_info']
        last_id = gd['last_id']
        last_id += 1
        self._storage.put('general_info', last_id = last_id)
        return last_id

    def add_note(self, note):
        """ Add note to database. """
        key = str(self.get_id()).zfill(6)
        d = self.make_dict(note)

        self._storage.put(key, **d)
        self.all_notes[key] = note
        self._keys[note] = key

    def update_note(self, note):
        """ Update the note in storage. """
        key = self._keys[note]
        if not self._storage.exists(key):
            raise KeyError("Such note doesn't exist")
        d = self.make_dict(note)
        self._storage.put(key, **d)

    def delete_note(self, note):
        """ Delete a note. """
        # get note's key
        key = self._keys[note]
        # delete from storage
        self._storage.delete(key)
        # del from _keys
        del self._keys[note]
        # del from all_notes
        del self.all_notes[key]

    def sorted_by_key(self):
        """ Yield all (key, note) tuples sorted by key."""
        return sorted(self.all_notes.items(), key=operator.itemgetter(0))

    @classmethod
    def make_dict(cls, note):
        """ Take a note and return a dict containing its details
        for saving to storage.
        """
        d = dict()
        d["date_created_str"] = datetime.strftime(note.date_created, cls.DATE_STR_FORMAT)
        d["text"] = note.text

        # include date modified if exists
        if note.date_modified:
            d["date_modified_str"] = datetime.strftime(note.date_modified, cls.DATE_STR_FORMAT)

        return d

    @classmethod
    def note_from_dict(cls, data):
        """ Take a dict from storage and construct note. """
        d = dict()
        d["date_created"] = datetime.strptime(data['date_created_str'], cls.DATE_STR_FORMAT)
        if "date_modified_str" in data:
            d["date_modified"] = datetime.strptime(data['date_modified_str'], cls.DATE_STR_FORMAT)
        d["text"] = data['text']

        # construct and return note
        return Note(**d)


DATABASE = NotesDB("notes_db.json")
