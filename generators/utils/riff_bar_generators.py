from mingus.containers import Bar, Note

from utils.utils import parse_note


def djent_bar4x4(rand, scale, is4x4 : bool = True) -> Bar:
    bar = Bar()
    notes = scale.ascending()
    bar.place_notes(parse_note("E1"), 8)
    for j in range(2, 16):
        cur_note = Note(notes[rand.randint(0, 22) % 6])
        bar.place_notes(cur_note, 16)

    return bar