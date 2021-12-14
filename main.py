# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time

import mingus.core.scales as scales
from mingus.containers import Note

import utils
from song.song import SongGenerator
from utils.config import ConfigData
from utils.midi_exporter import MidiExporter


def main():
    file = ConfigData.load_from_file()
    print(file.drumset_notes.kick)
    song = SongGenerator.generate_song(file, 'Devastation')
    MidiExporter.export_song(song)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
