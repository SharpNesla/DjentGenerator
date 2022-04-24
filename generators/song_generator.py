from __future__ import annotations

from enum import Enum, auto
from random import Random

from mingus.core.notes import int_to_note
from mingus.core.scales import *
from mingus.containers import Bar, Note

from generators.riffs.tommy_riff import tommy_riff
from song.parts import SongPartType, DrumPart, GuitarPart, SongPart
from song.song import Song
from utils.config import ConfigData
from utils.utils import enum_all_valuse_list, md5_from_str


class RiffType(Enum):
    SingleNotePoly: RiffType = auto()
    TomMuteRiff: RiffType = auto()


class RiffGenerator:
    @staticmethod
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
    def generate_riff(rand: Random, config : ConfigData, song: Song):
        sub_riffs = rand.randint(0, 1)

        bars_count = rand.randint(2, 4)

        riff_type = RiffType.TomMuteRiff

        match riff_type:
            case riff_type.TomMuteRiff:
                part = tommy_riff(rand, config, song)
        return part


class SongGenerator:
    @staticmethod
    def generate_song_part(rand: Random, config: ConfigData, song: Song, part_type: SongPartType) -> SongPart:
        part = None

        # Reseed random with part name and previous seed
        # to make possible recreation of separated song part
        rand.seed(md5_from_str(f'{song.salt}{part_type}{0}'))
        match part_type:
            case SongPartType.Riff:
                part = RiffGenerator.generate_riff(rand, config, song)
        return part

    @staticmethod
    def generate_song_structure(rand: Random) -> list[SongPartType]:
        parts = [SongPartType.Intro]

        song_verses_chorus_count = rand.randint(2, 3)

        parts.append(SongPartType)
        parts.append(SongPartType.Outro)

        return [SongPartType.Riff]

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

        song_parts = [SongGenerator.generate_song_part(rand, config, song, i) for i in structure]
        song.song_parts = song_parts
        return song

    @staticmethod
    def generate_progression():
        pass
