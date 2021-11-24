from __future__ import annotations

from enum import Enum, auto
from random import Random

from mingus.core.scales import *
from mingus.containers import Track, Bar
import yaml
import hashlib


class ConfigData(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Config'

    def __init__(self, BPMLowest=120, BPMHighest=120):
        self.BPMLowest = BPMLowest
        self.BPMHighest = BPMHighest


class SongPartType:
    Intro: SongPartType = auto(),
    Riff: SongPartType = auto(),
    BuildUp: SongPartType = auto()
    Verse: SongPartType = auto()
    Solo: SongPartType = auto()
    Outro: SongPartType = auto()


class DrumPartGenerators:
    @staticmethod
    def simple_part() -> DrumPart:
        part = DrumPart()
        standard_bar = Bar()
        standard_bar.place_notes('A', 4)
        part.bars = [standard_bar] * 4
        return part


class DrumPart:
    def __init__(self, bars=None):
        if bars is None:
            bars = []
        self.bars = bars


class GuitarPart:
    def __init__(self, bars=None):
        if bars is None:
            bars = []
        self.bars = bars


class SongPart:
    def __init__(self,
                 part_type: SongPartType,
                 guitar_part=None,
                 bass_part=None,
                 solo_guitar_part=None,
                 super_reverb_part=None,
                 drum_part: DrumPart = None):
        self.super_reverb_part = super_reverb_part
        self.solo_guitar_part = solo_guitar_part
        self.bass_part = bass_part
        self.guitar_part = guitar_part
        self.drum_part = drum_part
        self.part_type = part_type


class Song:
    def __init__(self, scale: list[str], name='', salt=0, bpm=120, song_parts: list[SongPart] = None,
                 song_structure: list[SongPartType] = None):
        if song_parts is None:
            self.song_parts = []
        if song_structure is None:
            self.song_structure = []
        self.song_structure = song_structure
        self.salt = salt
        self.name = name
        self.scale = scale
        self.bpm = bpm


class RiffType(Enum):
    TomMuteRiff: RiffType = auto()


class RiffGenerator:
    @staticmethod
    def generate_solo_part(rand: Random) -> GuitarPart:
        solo = GuitarPart()
        scale = NaturalMinor('E', 4)
        notes = scale.ascending()
        bar_list = []
        for i in range(0, rand.randint(2, 4)):
            bar = Bar()

            bar.place_notes(notes[0], 16)
            for i in range(1, 15):
                bar.place_notes(notes[rand.randint(0, 16)], 16)

            bar.place_notes(notes[0], 16)

            bar_list.append(bar)

        part = GuitarPart(bar_list)
        return part

    @staticmethod
    def generate_drum_part(rand: Random, part_type) -> DrumPart:
        drums = None
        if part_type == SongPartType.Riff:
            drums = DrumPartGenerators.simple_part()
        return drums

    @staticmethod
    def generate_riff(rand: Random):
        sub_riffs = rand.randint(0, 1)

        for i in range(0, sub_riffs):
            pass
        drum_part = RiffGenerator.generate_drum_part(rand, SongPartType.Riff)
        solo_part = RiffGenerator.generate_solo_part(rand)
        part = SongPart(SongPartType.Riff,
                        GuitarPart(),
                        GuitarPart(),
                        solo_part,
                        GuitarPart(),
                        drum_part)
        return part


class SongGenerator:
    @staticmethod
    def generate_song_part(rand: Random, part_type: SongPartType) -> SongPart:
        part = None
        match part_type:
            case SongPartType.Riff:
                part = RiffGenerator.generate_riff(rand)
        return part

    @staticmethod
    def generate_song_structure(rand: Random) -> list[SongPartType]:
        parts = [SongPartType.Intro]

        song_verses_chorus_count = rand.randint(2, 3)

        parts.append(SongPartType)

        return [SongPartType.Riff]

    @staticmethod
    def generate_song(config: ConfigData, name='', salt=0):
        rand = Random()
        seed = int(hashlib.md5((name + str(salt)).encode('utf-8')).hexdigest(), 16)
        rand.seed(seed)

        low_note = 'E'

        bpm = rand.randint(config.BPMLowest, config.BPMHighest)
        modes = [NaturalMinor, Major, Phrygian, Lydian]
        scale = None
        while True:
            root_note = Chromatic('C').ascending()[rand.randint(0, 11)]
            scale = modes[rand.randint(0, 3)](root_note)
            if low_note in scale.ascending():
                break

        # structure = SongGenerator.generate_song_structure(rand)
        structure = [SongPartType.Riff]
        song = Song([], name, salt, bpm, structure)
        song_parts = [SongGenerator.generate_song_part(rand, structure[0])]
        song.song_parts = song_parts
        return song
