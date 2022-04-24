from generators.song_generator import SongGenerator
from utils.config import ConfigData
from utils.midi_exporter import MidiExporter


def main():
    file = ConfigData.load_from_file()
    song = SongGenerator.generate_song(file, 'Kind')
    MidiExporter.export_song(song)


if __name__ == '__main__':
    main()
