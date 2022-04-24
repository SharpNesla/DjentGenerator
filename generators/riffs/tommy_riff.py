from random import Random

from mingus.containers import Bar

from generators.generic.silence_generator import generate_silence
from generators.generic.solo_generators import generate_solo_part
from generators.utils.drum_generators import tommy_drums
from song.song import Song
from song.parts import SongPartType, DrumPart, SongPart
from utils.config import ConfigData

def tommy_riff(rand: Random, config: ConfigData, song: Song) -> SongPart:
    drum_part = tommy_drums(rand, config, song)
    solo_part = generate_solo_part(rand, song.scale, len(drum_part.bars))

    part = SongPart(SongPartType.Riff,
                    solo_part,
                    solo_part,
                    solo_part,
                    solo_part,
                    drum_part)

    return part
