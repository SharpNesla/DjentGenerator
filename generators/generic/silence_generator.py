from mingus.containers import Bar

from song.parts import MidiPart


def generate_silence(bars_count) -> MidiPart:
    part = MidiPart()

    for i in range(0, bars_count):
        bar = Bar()
        bar.place_rest(1)
        part.bars.append(bar)

    return part
