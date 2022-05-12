import itertools

from mingus.containers import Track, Bar, NoteContainer


def humanize_midi(track: Track,
                  velocity: (int, int),
                  timing_begin: (float, float),
                  timing_end: (float, float)) -> Track:
    for note_cont in itertools.chain(track.bars):
        pass
    return track
