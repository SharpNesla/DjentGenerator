# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time

import mingus.core.scales as scales

from song import SongGenerator, ConfigData
from midi_exporter import MidiExporter


def main():
    MidiExporter.export_song(SongGenerator.generate_song(ConfigData()), 'test.mid')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
