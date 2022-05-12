from abc import abstractmethod, ABC
from random import Random

from song.parts import SongPartType, SongPart
from song.song import Song
from utils.config import ConfigData


class PartGenerator(ABC):
    @abstractmethod
    @property
    def type(self) -> SongPartType:
        return SongPartType.Riff

    @staticmethod
    @abstractmethod
    def generate_part(self, rand: Random, config: ConfigData, song: Song) -> SongPart:
        raise NotImplementedError('Implement method!')