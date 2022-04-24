from __future__ import annotations

from enum import auto


class SongPartType:
    Intro: SongPartType = auto(),
    Riff: SongPartType = auto(),
    BuildUp: SongPartType = auto()
    Verse: SongPartType = auto()
    Solo: SongPartType = auto()
    Outro: SongPartType = auto()


class MidiPart:
    def __init__(self, bars=None):
        if bars is None:
            bars = []
        self.bars = bars


class DrumPart(MidiPart):
    def __init__(self, bars=None):
        super().__init__(bars)


class GuitarPart(MidiPart):
    def __init__(self, bars=None):
        super().__init__(bars)


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
