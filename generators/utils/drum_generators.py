from random import Random

from mingus.containers import Bar

from song.song import Song
from song.parts import DrumPart, SongPart
from utils.config import ConfigData


# TODO rewrite with correct algo
def every_kick_strong_snare(rand: Random, config: ConfigData, part: SongPart, song: Song) -> DrumPart:
    drumset = config.drumset_notes
    part = DrumPart()
    bar_list = []
    for i in range(0, 4):
        bar = Bar()

        for i in range(0, 8):
            # 8 kick note
            if i % 8 == 0:
                note = drumset.snare
                note.velocity = 127
                bar.place_notes(note, 8)
            else:
                note = drumset.kick
                note.velocity = 127
                bar.place_notes(note, 8)

            if i % 2 == 0:
                note = drumset.china
                note.velocity = 127
                bar.place_notes(note, 8)
        bar_list.append(bar)
    part.bars = bar_list
    return part


def bar_place_notes_at(self, notes, at):
    for x in self.bar:
        attr = x[0]
        if x[0] == at:
            x[2] += notes


def bar_replace_notes_at(self, notes, at):
    for x in self.bar:
        attr = x[0]
        if x[0] == at:
            x[2].notes = notes


# def tommy_drums(rand: Random, config: ConfigData, song: Song) -> DrumPart:
#     drumset = config.drumset_notes
#     part = DrumPart()
#     toms = [drumset.snare,
#             drumset.rack_tom,
#             drumset.floor_tom_1,
#             drumset.floor_tom_2]
#
#     bar_list = []
#     for i in range(0, 4):
#         bar = Bar()
#         # Toms, kick, snares
#         for j in range(0, 4):
#             note = drumset.kick
#             bar.place_notes(note, 16)
#             for k in range(1, 3):
#                 selected_tom = rand.randint(1, 3)
#                 if selected_tom == 3:
#                     bar_replace_notes_at(bar, [toms[selected_tom]], 1 / 16 * k)
#                 else:
#                     bar_replace_notes_at(bar, [drumset.kick, toms[selected_tom]], 1 / 16 * k)
#
#         note = drumset.snare
#         if i % rand.randint(2, 3) * 2 == 0:
#             bar_replace_notes_at(bar, [drumset.snare], 0)
#         # Cymbals
#         if i % rand.randint(3, 4) * 2 == 0:
#             bar_place_notes_at(bar, [drumset.crash_left], 0)
#
#         if i % rand.randint(4,8) * 2 == 0:
#             bar_replace_notes_at(bar, [
#                 drumset.kick,
#                 drumset.crash_left,
#                 drumset.crash_right], 0)
#         # China and ride
#         if rand.randint(0, 7) == 0:
#             offbeat_snare = rand.randint(0,7) == 0
#             if offbeat_snare:
#                 bar_replace_notes_at(bar, [drumset.kick, drumset.china], 1/16 * rand.randint(1,8))
#             else:
#                 bar_replace_notes_at(bar, [drumset.snare, drumset.china], 1/16 * rand.randint(1,8))
#
#         if rand.randint(0, 7) == 0:
#             offbeat_snare = rand.randint(0,7) == 0
#             if offbeat_snare:
#                 bar_replace_notes_at(bar, [drumset.kick, drumset.ride], 1/8 * rand.randint(1,4 ))
#             else:
#                 bar_replace_notes_at(bar, [drumset.snare, drumset.ride], 1/16 * rand.randint(1,8))
#
#         bar_list.append(bar)
#
#     part.bars = bar_list
#     return part

def tommy_drums(rand: Random, config: ConfigData, song: Song) -> DrumPart:
    drumset = config.drumset_notes
    part = DrumPart()
    toms = [drumset.snare,
            drumset.rack_tom,
            drumset.floor_tom_1,
            drumset.floor_tom_2]

    bar_list = []
    for i in range(0, 16 ):
        bar = Bar()
        # Toms, kick, snares
        for j in range(0, 4):
            note = drumset.kick
            bar.place_notes(note, 16)
            for k in range(1, 3):
                selected_tom = rand.randint(1, 3)
                if selected_tom == 3:
                    bar_replace_notes_at(bar, [toms[selected_tom]], 1 / 16 * k)
                else:
                    bar_replace_notes_at(bar, [drumset.kick, toms[selected_tom]], 1 / 16 * k)

        note = drumset.snare
        if i % rand.randint(2, 3) * 2 == 0:
            bar_replace_notes_at(bar, [drumset.snare], 0)
        # Cymbals
        if i % rand.randint(3, 4) * 2 == 0:
            bar_place_notes_at(bar, [drumset.crash_left], 0)

        if i % rand.randint(4,8) * 2 == 0:
            bar_replace_notes_at(bar, [
                drumset.kick,
                drumset.crash_left,
                drumset.crash_right], 0)
        # China and ride
        if rand.randint(0, 7) == 0:
            offbeat_snare = rand.randint(0,7) == 0
            if offbeat_snare:
                bar_replace_notes_at(bar, [drumset.kick, drumset.china], 1/16 * rand.randint(1,8))
            else:
                bar_replace_notes_at(bar, [drumset.snare, drumset.china], 1/16 * rand.randint(1,8))

        if rand.randint(0, 7) == 0:
            offbeat_snare = rand.randint(0,7) == 0
            if offbeat_snare:
                bar_replace_notes_at(bar, [drumset.kick, drumset.ride], 1/8 * rand.randint(1,4 ))
            else:
                bar_replace_notes_at(bar, [drumset.snare, drumset.ride], 1/16 * rand.randint(1,8))

        bar_list.append(bar)

    part.bars = bar_list
    return part