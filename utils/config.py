from __future__ import annotations

import yaml
from mingus.containers import Note

from utils.utils import dict_to_class


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


class ConfigData(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    drumset_notes: DrumSetConfig

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
                print('ok')
            except yaml.YAMLError as exc:
                print(exc)

        return data
