from __future__ import annotations

from enum import Enum, auto
from random import Random

import mingus.core.scales
from mingus.core.notes import int_to_note
from mingus.core.scales import *
from mingus.containers import Track, Bar, Note
import yaml

from utils.config import ConfigData
from utils.utils import enum_all_valuse_list, md5_from_str

_DEFAULT_KS = 'C0'


class SongPartType:
    Intro: SongPartType = auto(),
    Riff: SongPartType = auto(),
    BuildUp: SongPartType = auto()
    Verse: SongPartType = auto()
    Solo: SongPartType = auto()
    Outro: SongPartType = auto()


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
    def __init__(self, scale: mingus.core.scales._Scale, name='', salt=0, bpm=120, song_parts: list[SongPart] = None,
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
    SingleNotePoly: RiffType = auto()
    TomMuteRiff: RiffType = auto()


class RiffGenerator:
    @staticmethod
    def generate_solo_part(rand: Random, scale, bars_count) -> GuitarPart:
        notes = scale.ascending()
        bar_list = []
        for i in range(0, bars_count):
            bar = Bar()

            movement = rand.randint(0, 30)

            # Tonic
            bar.place_notes(notes[0], 16)
            cur_note = Note(notes[0])

            for j in range(1, 15):
                # bar.place_notes(notes[rand.randint(0, 22) % 6], 16)

                # Solo movement (up, down, random_notes)

                # match movement:
                #     case 0:
                #         cur_note = Note(notes[(notes.index(cur_note.name) + 1) % 6], 4)
                #         bar.place_notes(cur_note, 16)
                #     case 1:
                #         cur_note = Note(notes[(notes.index(cur_note.name) - 1) % 6], 4)
                #         bar.place_notes(cur_note, 16)
                #     case 2:
                #
                cur_note = Note(notes[rand.randint(0, 22) % 6])
                bar.place_notes(cur_note, 16)
                # Amount of notes in phrase (notes * repeats)
                amount_of_notes = rand.randint(3, 4) * rand.randint(1, 2)

            # End Tonic
            bar.place_notes(notes[0], 16)

            bar_list.append(bar)

        part = GuitarPart(bar_list)
        return part

    @staticmethod
    def generate_drum_part(rand: Random, bars_count) -> DrumPart:
        part = DrumPart()
        bar_list = []
        for i in range(0, bars_count):
            bar = Bar()

            for i in range(0, 8):
                # 8 kick note
                if i % 8 == 0:
                    note = Note('D', 1)
                    note.velocity = 127
                    bar.place_notes(note, 8)
                else:
                    note = Note('C', 1)
                    note.velocity = 127
                    bar.place_notes(note, 8)

                if i % 2 == 0:
                    note = Note('E', 5)
                    note.velocity = 127
                    bar.place_notes(note, 8)
            bar_list.append(bar)
        part.bars = bar_list
        return part

    def generate_guitar_part(rand: Random, scale, bars_count) -> GuitarPart:
        notes = scale.ascending()
        bar_list = []
        for i in range(0, bars_count):
            bar = Bar()

            movement = rand.randint(0, 30)

            # Tonic
            bar.place_notes(Note(notes[0], 1, velocity=127), 8)
            cur_note = Note(notes[0])

            for j in range(1, 7):
                cur_note = Note(notes[rand.randint(0, 22) % 6], 2, velocity=127)
                bar.place_notes(cur_note, 8)

            # End Tonic
            bar.place_notes(Note(notes[0], 1, velocity=127), 8)

            bar_list.append(bar)

        part = GuitarPart(bar_list)
        return part

    @staticmethod
    def generate_riff(rand: Random, song: Song):
        sub_riffs = rand.randint(0, 1)

        bars_count = rand.randint(2, 4)

        riff_types = enum_all_valuse_list(RiffType)

        for i in range(0, sub_riffs):
            pass
        drum_part = RiffGenerator.generate_drum_part(rand, bars_count)
        solo_part = RiffGenerator.generate_solo_part(rand, song.scale, bars_count)
        guitar_part = RiffGenerator.generate_guitar_part(rand, song.scale, bars_count)
        part = SongPart(SongPartType.Riff,
                        guitar_part,
                        guitar_part,
                        solo_part,
                        solo_part,
                        drum_part)
        return part


class SongGenerator:
    @staticmethod
    def generate_song_part(rand: Random, song: Song, part_type: SongPartType) -> SongPart:
        part = None

        # Reseed random with part name and previous seed
        # to make possible recreation of separated song p0000art

        match part_type:
            case SongPartType.Riff:
                part = RiffGenerator.generate_riff(rand, song)
        return part

    @staticmethod
    def generate_song_structure(rand: Random) -> list[SongPartType]:
        parts = [SongPartType.Intro]

        song_verses_chorus_count = rand.randint(2, 3)

        parts.append(SongPartType)

        parts.append(SongPartType.Outro)

        return [SongPartType.Riff, SongPartType.Riff]

    @staticmethod
    def generate_song(config: ConfigData, name='', salt=0):
        rand = Random()
        seed = md5_from_str(name + str(salt))
        rand.seed(seed)

        low_note = 'E'

        bpm = 120  # rand.randint(config.BPMLowest, config.BPMHighest)
        modes = [NaturalMinor, Major, Phrygian, Lydian]
        scale = None
        while True:
            root_note = int_to_note(rand.randint(0, 11))
            scale = modes[rand.randint(0, 3)](root_note)
            if low_note in scale.ascending():
                break

        # structure = SongGenerator.generate_song_structure(rand)
        structure = SongGenerator.generate_song_structure(rand)
        song = Song(scale, name, salt, bpm, structure)

        song_parts = [SongGenerator.generate_song_part(rand, song, i) for i in structure]
        song.song_parts = song_parts
        return song

    @staticmethod
    def generate_progression():
        pass
