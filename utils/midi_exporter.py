from mingus.containers import Track, Composition
from mingus.midi import midi_file_out, midi_track
from song.song import Song, SongPart, DrumPart


class MidiExporter:
    @staticmethod
    def build_song(song: Song) -> Composition:
        composition = Composition()

        # TODO: make workaround about this messy code
        drum_track = Track()
        guitar_track = Track()
        bass_track = Track()
        solo_guitar_track = Track()
        super_reverb_track = Track()

        drum_track.name = 'drum_track'
        guitar_track.name = 'guitar_track'
        bass_track.name = 'bass_track'
        solo_guitar_track.name = 'solo_track'
        super_reverb_track.name = 'super_reverb_track'

        for part in song.song_parts:
            for bar in part.drum_part.bars:
                drum_track.add_bar(bar)
            for bar in part.guitar_part.bars:
                guitar_track.add_bar(bar)
            for bar in part.bass_part.bars:
                bass_track.add_bar(bar)
            for bar in part.solo_guitar_part.bars:
                solo_guitar_track.add_bar(bar)
            for bar in part.super_reverb_part.bars:
                super_reverb_track .add_bar(bar)

        composition.add_track(drum_track)
        composition.add_track(guitar_track)
        composition.add_track(bass_track)
        composition.add_track(solo_guitar_track)
        composition.add_track(super_reverb_track)

        return composition

    @staticmethod
    def export_song(song: Song, filename: str = None):
        composition = MidiExporter.build_song(song)

        if filename is None:
            filename = f'{song.name}_({song.scale.name}_{song.bpm}BPM).mid'.replace(' ', '_')

        midi_file_out.write_Composition(filename, composition, bpm=90)
