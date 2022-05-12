from random import Random

from generators.generic.solo_generators import generate_solo_part, updown_weighted_solo
from generators.utils.drum_generators import tommy_drums
from song.song import Song
from song.parts import SongPartType, SongPart
from utils.config import ConfigData
from utils.guitar_simulator import GuitarSimulator


def tommy_riff(rand: Random, config: ConfigData, song: Song) -> SongPart:
    guit = GuitarSimulator(config.guitar)
    drum_part = tommy_drums(rand, config, song)
    solo_part = generate_solo_part(rand, song.scale, len(drum_part.bars))
    solo_part2 = guit.play(updown_weighted_solo(rand, song.scale, len(drum_part.bars)))
    part = SongPart(SongPartType.Riff,
                    solo_part,
                    solo_part,
                    solo_part2,
                    solo_part2,
                    drum_part)

    return part
