import hashlib
import re
from enum import Enum
from collections import namedtuple
from mingus.containers import Note
from yaml import YAMLObject


def md5_from_str(string: str) -> int:
    return int(hashlib.md5(string.encode('utf-8')).hexdigest(), 16)


def enum_all_valuse_list(enum_instance: Enum):
    return list(map(lambda c: c.value, enum_instance))


def parse_note(note_oct_string: str):
    octave = int(re.findall(r'-?\d+$', note_oct_string)[0])
    note = re.findall(r'^[A-G]#?', note_oct_string)[0]
    # Default velocity is 127
    return Note(note, octave, velocity=127)


def transpose_note(note: Note, interval: int) -> Note:
    return Note().from_int(int(note) + interval)


def clone_note(note: Note):
    return Note(note.name, note.octave)


def dict_to_class(class_type, dictionary):
    # Applies to Python-3 Standard Library
    class Struct(YAMLObject):
        def __init__(self, data):
            for name, value in data.items():
                setattr(self, name, self._wrap(value))

        def _wrap(self, value):
            if isinstance(value, (tuple, list, set, frozenset)):
                return type(value)([self._wrap(v) for v in value])
            else:
                return Struct(value) if isinstance(value, dict) else value

    obj = Struct(dictionary)
    obj.__class__ = class_type
    return obj
