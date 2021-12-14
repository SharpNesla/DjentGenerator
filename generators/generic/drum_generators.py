from mingus.containers import Bar

from song import DrumPart


def blastbeat():
    pass


def simple_part() -> DrumPart:
    part = DrumPart()
    standard_bar = Bar()
    standard_bar.place_notes('A', 4)
    part.bars = [standard_bar] * 4
    return part
