from note import Note
from customdatetime import DT
from kivy.storage.jsonstore import JsonStore


def read_old_notes(file):
    with open(file, encoding='utf-8') as f:
        buff = []
        for line in f.readlines():
            if line.startswith('- - - - -'):
                yield make_note_from_lines(buff)
                del buff[:]
            else:
                buff.append(line.strip())


def make_note_from_lines(buff):
    if not buff[0].isspace():
        buff.pop(0)
    dt_string = buff[0] + ', ' + buff[1].split(', ')[1]
    date_created = DT.from_str(dt_string, FORMAT="%B %d, %Y, %H:%M")
    text = '\n'.join(buff[3:])
    return Note(text=text, date_created=date_created)


if __name__ == "__main__":
    storage = JsonStore('old_notes.json', indent=True)
    for note in read_old_notes("MyNotes_20180113_1045.txt"):
        note.save_to_storage(storage)
