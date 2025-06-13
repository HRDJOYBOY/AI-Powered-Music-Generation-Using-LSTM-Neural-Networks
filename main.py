from mido import MidiFile, MidiTrack, Message

def parse_midi_notes(file_path):
    """
    Parse a MIDI file and extract note_on events into a list of dictionaries.
    """
    mid = MidiFile(file_path)
    notes = []

    for i, track in enumerate(mid.tracks):
        time = 0
        for msg in track:
            time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append({
                    'note': msg.note,
                    'velocity': msg.velocity,
                    'time': time,
                    'track': i
                })
                time = 0  # Reset time after each note event
    return notes


def save_notes_to_midi(notes, output_file):
    """
    Convert list of note dictionaries back to a MIDI file and save it.
    """
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    for note in notes:
        track.append(Message('note_on', note=note['note'],
                             velocity=note['velocity'],
                             time=note['time']))

    mid.save(output_file)
    print(f"\n✅ Saved new MIDI file as: {output_file}")


# 🚀 Example usage
if __name__ == "__main__":
    input_file = r'C:\Users\haris\music generation with ai\maestro-midi\maestro-v3.0.0\2004\MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi'  # Replace this with your MIDI file path
    output_file = 'output.mid'

    print(f"🔍 Parsing MIDI file: {input_file}")
    note_data = parse_midi_notes(input_file)

    print(f"\n🎵 Extracted {len(note_data)} notes. First 5:")
    for note in note_data[:5]:
        print(note)

    save_notes_to_midi(note_data, output_file)
from mido import MidiFile, MidiTrack, Message
import json

def parse_midi_notes(file_path):
    """
    Parse a MIDI file and extract note_on events into a list of dictionaries.
    """
    mid = MidiFile(file_path)
    notes = []

    for i, track in enumerate(mid.tracks):
        time = 0
        for msg in track:
            time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append({
                    'note': msg.note,
                    'velocity': msg.velocity,
                    'time': time,
                    'track': i
                })
                time = 0  # Reset time after each note event
    return notes

def save_notes_to_midi(notes, output_file):
    """
    Convert list of note dictionaries back to a MIDI file and save it.
    """
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    for note in notes:
        track.append(Message('note_on', note=note['note'],
                             velocity=note['velocity'],
                             time=note['time']))

    mid.save(output_file)
    print(f"\n✅ Saved new MIDI file as: {output_file}")

def save_notes_to_json(notes, json_path='note_data.json'):
    """
    Save extracted notes to a JSON file for training.
    """
    with open(json_path, 'w') as f:
        json.dump(notes, f)
    print(f"\n✅ Saved notes to JSON file: {json_path}")

# 🚀 Example usage
if __name__ == "__main__":
    input_file = r'C:\Users\haris\music generation with ai\maestro-midi\maestro-v3.0.0\2004\MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi'
    output_file = 'output.mid'

    print(f"🔍 Parsing MIDI file: {input_file}")
    note_data = parse_midi_notes(input_file)

    print(f"\n🎵 Extracted {len(note_data)} notes. First 5:")
    for note in note_data[:5]:
        print(note)

    save_notes_to_midi(note_data, output_file)
    save_notes_to_json(note_data, 'note_data.json')  # 🆕 This line is critical
