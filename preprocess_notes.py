# preprocess_notes.py
import json
import numpy as np
from sklearn.preprocessing import LabelEncoder

def load_notes(json_path='note_data.json'):
    """
    Load notes from a JSON file and return a list of note strings.
    """
    with open(json_path, 'r') as f:
        note_data = json.load(f)
    return [str(n['note']) for n in note_data]

def prepare_sequences(notes, seq_length=50):
    """
    Prepare input and target sequences for model training.
    Returns input sequences, target notes, number of unique notes, and the encoder.
    """
    if not notes:
        raise ValueError("Notes list is empty.")

    encoder = LabelEncoder()
    note_int = encoder.fit_transform(notes)

    input_seq = []
    target_seq = []

    for i in range(len(note_int) - seq_length):
        input_seq.append(note_int[i:i + seq_length])
        target_seq.append(note_int[i + seq_length])

    return (
        np.array(input_seq),
        np.array(target_seq),
        len(encoder.classes_),
        encoder
    )
def create_note_mappings(notes):
    unique_notes = sorted(set(note['note'] for note in notes))
    note_to_int = {note: i for i, note in enumerate(unique_notes)}
    int_to_note = {i: note for note, i in note_to_int.items()}
    return note_to_int, int_to_note
