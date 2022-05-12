from random import Random

from mingus.containers import Bar, Note

from song.parts import GuitarPart


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

def updown_weighted_solo(rand: Random, scale, bars_count) -> GuitarPart:
    notes = scale.ascending()
    upper_oct = 48
    lower_oct = 0
    position = 32
    bar = Bar()
    bar.length = 32
    for i in range(0, bars_count):

        bar.place_notes(notes[0], 16)

        for j in range(0, 15):
            movement = rand.randint(0, 1)
            if movement == 0:
                position += 1
            else:
                position -= 1
            cur_note = Note(notes[position % len(notes)], position // len(notes))
            bar.place_notes(cur_note, 16)

    part = GuitarPart([bar])
    return part