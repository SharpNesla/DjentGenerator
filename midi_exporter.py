from mingus.containers import Track, Composition
from mingus.midi import midi_file_out, midi_track
from song import Song, SongPart, DrumPart


class MidiExporter:

    @staticmethod
    def build_song(song: Song) -> Composition:
        composition = Composition()

        drum_track = Track()

        drum_track.name = 'drum_track'
        for part in song.song_parts:
            for bar in part.drum_part.bars:
                drum_track.add_bar(bar)

        composition.add_track(drum_track)
        return composition

    @staticmethod
    def export_song(song: Song, filename: str):
        composition = MidiExporter.build_song(song)
        midi_file_out.write_Composition(filename, composition, bpm=song.bpm)