from __future__ import annotations

from enum import Enum, auto
from random import Random
from mingus.containers import Track, Bar
import yaml


class ConfigData(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Config'

    def __init__(self, BPMLowest=120, BPMHighest=120):
        self.BPMLowest = BPMLowest
        self.BPMHighest = BPMHighest


class SongPartType:
    Intro = auto(),
    Riff = auto(),
    BuildUp = auto()
    Verse = auto()
    Solo = auto()


class DrumPartGenerators:
    @staticmethod
    def simple_part() -> DrumPart:
        part = DrumPart()
        standard_bar = Bar()
        standard_bar.place_notes('A', 4)
        part.bars = [standard_bar] * 4
        return part


class DrumPart:
    def __init__(self, bars: [Bar] = None):
        self.bars = bars


class GuitarPart:
    def __init__(self):
        pass


class SongPart:
    def __init__(self, part_type: SongPartType, guitar_part=None, drum_part: DrumPart = None):
        self.guitar_part = guitar_part
        self.drum_part = drum_part
        self.part_type = part_type


class Song:
    def __init__(self, scale: [str], name='', salt=0, bpm=120, song_parts: list[SongPart] = None,
                 song_structure=None):
        if song_parts is None:
            self.song_parts = []
        if song_structure is None:
            self.song_structure = []
        self.song_structure = song_structure
        self.salt = salt
        self.name = name
        self.scale = scale
        self.bpm = bpm


class SongGenerator:
    @staticmethod
    def generate_drum_part(random_instance: Random, part: SongPart) -> DrumPart:
        drums = None
        if part.part_type == SongPartType.Riff:
            drums = DrumPartGenerators.simple_part()
        return drums

    @staticmethod
    def generate_song_part(random_instance: Random, part_type: SongPartType) -> SongPart:
        part = SongPart(part_type)
        drums = SongGenerator.generate_drum_part(random_instance, part)
        part.drum_part = drums
        return part

    @staticmethod
    def generate_song_structure(random_instance: Random) -> list[SongPartType]:
        return [SongPartType.Riff]

    @staticmethod
    def generate_song(config: ConfigData, name='', salt=0):
        rand = Random()
        rand.seed(name + str(salt))

        bpm = rand.randint(config.BPMLowest, config.BPMHighest)
        structure = SongGenerator.generate_song_structure(rand)
        song = Song([], name, salt, bpm, structure)
        song_parts = [SongGenerator.generate_song_part(rand, structure[0])]
        song.song_parts = song_parts
        return song
