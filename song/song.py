from __future__ import annotations

import mingus.core.scales

from song.parts import SongPart, SongPartType


class Song:
    def __init__(self, scale: mingus.core.scales._Scale,
                 name='', salt=0,
                 bpm=120,
                 song_parts: list[SongPart] = None,
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
