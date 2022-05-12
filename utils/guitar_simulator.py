import copy

from mingus.containers import Bar, NoteContainer, Note

from song.parts import GuitarPart
from utils.config import GuitarConfig
from utils.utils import transpose_note

GUITARIST_HAND_STRETCH: int = 5


class GuitarSimulator:
    neutral_hand_position: int
    current_hand_position: int
    guitar_config: GuitarConfig

    fretboard: [[Note]]

    def __init__(self, guitar_config: GuitarConfig, idle_hand_position: int = 17):
        self.current_hand_position = idle_hand_position
        self.neutral_hand_position = idle_hand_position
        self.guitar_config = guitar_config
        tuning = guitar_config.tuning
        self.fretboard = [[transpose_note(root, i) for root in tuning] for i in range(0, 25)]

    def get_(self, note: Note, hand_position: int) -> int:
        current_position_notes = self.fretboard[hand_position:hand_position + 5]

        string_number = -1

        for current_fret in current_position_notes:
            for idx, current_fret_note in enumerate(current_fret):
                # Second condition: if notes played by 7-8 string for high positions
                # prefer to change position.
                if int(current_fret_note) == int(note):
                    # if hand_position > 12 and idx > 5:
                    #     return -1
                    string_number = idx
                    break

        return string_number

    def find_position(self, note: Note, last_string: int) -> (int, int):
        # First algo: bruteforce
        hand_position = 0
        string_number = -1

        for i in range(19, 0, -1):
            string_number = self.get_(note, i)
            if string_number != -1:
                hand_position = i
                break

        # Second algo: change position with the same string as previous.
        # Algo applies when distance between found and neutral fret lower than bruteforced.
        for i in range(19, 0, -1):
            current_position_notes = self.fretboard[i: + 5]
            for current_fret in current_position_notes:
                if int(current_fret[last_string]) == int(note) and \
                        abs(self.neutral_hand_position - i) < abs(self.neutral_hand_position - hand_position):
                    # if i > 12 and last_string > 5:
                    #     continue
                    string_number = last_string
                    hand_position = i
                    break

        return hand_position, string_number

    def play(self, part: GuitarPart) -> GuitarPart:
        part = copy.deepcopy(part)

        last_string_number = 2

        for bar in part.bars:
            for bar_ in bar.bar:
                _, _, note_container = bar_
                if len(note_container) == 1:
                    cont: NoteContainer = note_container
                    current_string_number = self.get_(cont.notes[0], self.current_hand_position)
                    if current_string_number == -1:
                        hand_post, current_string_number = self.find_position(cont.notes[0], last_string_number)
                        self.current_hand_position = hand_post
                    last_string_number = current_string_number
                    cont.add_note(self.guitar_config.ks_strings[current_string_number])
                else:
                    pass
        return part
