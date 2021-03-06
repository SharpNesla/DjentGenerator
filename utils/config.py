from __future__ import annotations

import yaml
from mingus.containers import Note

from utils.utils import dict_to_class, parse_note


class DrumSetConfig(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = '!drumset'
    kick: Note
    snare: Note
    rack_tom: Note
    floor_tom_1: Note
    floor_tom_2: Note
    hat_closed: Note
    hat_open: Note
    crash_left: Note
    crash_right: Note
    ride: Note
    china: Note

class GuitarConfig(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = '!guitar'
    tuning: [Note]

    # Key switches
    ks_sustain: Note
    ks_mute: Note
    ks_tapping: Note

    # Key switches for strings, from 1 to n-th string
    ks_strings: [Note]
    ks_strings_off: Note


class ConfigData(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    drumset_notes: DrumSetConfig
    guitar: GuitarConfig

    def __init__(self, drumset_notes: DrumSetConfig = None):
        if drumset_notes is None:
            self.drumset_notes = DrumSetConfig()

    @staticmethod
    def load_from_file(filename: str = 'config.yaml') -> ConfigData:
        # TODO: rewrite with workarounds about correct typings
        data: ConfigData = ConfigData()

        with open(filename, "r") as stream:
            try:
                yaml.add_constructor('!drumset', DrumSetConfig.__init__)
                data = dict_to_class(ConfigData, yaml.safe_load(stream))
                data.drumset_notes.kick = parse_note(data.drumset_notes.kick)
                data.drumset_notes.snare = parse_note(data.drumset_notes.snare)
                data.drumset_notes.rack_tom = parse_note(data.drumset_notes.rack_tom)
                data.drumset_notes.floor_tom_1 = parse_note(data.drumset_notes.floor_tom_1)
                data.drumset_notes.floor_tom_2 = parse_note(data.drumset_notes.floor_tom_2)
                data.drumset_notes.hat_closed = parse_note(data.drumset_notes.hat_closed)
                data.drumset_notes.hat_open = parse_note(data.drumset_notes.hat_open)
                data.drumset_notes.crash_left = parse_note(data.drumset_notes.crash_left)
                data.drumset_notes.crash_right = parse_note(data.drumset_notes.crash_right)
                data.drumset_notes.ride = parse_note(data.drumset_notes.ride)
                data.drumset_notes.china = parse_note(data.drumset_notes.china)

                yaml.add_constructor('!guitar', DrumSetConfig.__init__)
                if len(data.guitar.tuning) != len(data.guitar.ks_strings):
                    raise Exception('Incorrect strings KS-s amount')

                data.guitar.tuning = [parse_note(x) for x in data.guitar.tuning]
                data.guitar.ks_sustain = parse_note(data.guitar.ks_sustain)
                data.guitar.ks_mute = parse_note(data.guitar.ks_mute)
                data.guitar.ks_tapping = parse_note(data.guitar.ks_tapping)
                data.guitar.ks_strings_off = parse_note(data.guitar.ks_strings_off)
                data.guitar.ks_strings = [parse_note(x) for x in data.guitar.ks_strings]

            except yaml.YAMLError as exc:
                print(exc)

        return data
