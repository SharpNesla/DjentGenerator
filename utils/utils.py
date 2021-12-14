import hashlib
from enum import Enum
from collections import namedtuple
from mingus.containers import Note
from yaml import YAMLObject


def md5_from_str(string: str) -> int:
    return int(hashlib.md5(string.encode('utf-8')).hexdigest(), 16)


def enum_all_valuse_list(enum_instance: Enum):
    return list(map(lambda c: c.value, enum_instance))


def parse_note(note_oct_string: str):
    octave = note_oct_string[-1:]
    note = note_oct_string[:-1]

    return Note(note, octave)


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
