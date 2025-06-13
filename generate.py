import json
import numpy as np
import random
from keras.models import load_model
from mido import MidiFile, MidiTrack, Message
from preprocess_notes import create_note_mappings

# Load trained model
model = load_model('note_lstm_model.h5')

# Load notes
with open('note_data.json', 'r') as f:
    notes = json.load(f)

sequence_length = 50
note_dicts = notes if isinstance(notes[0], dict) else [{'note': n} for n in notes]
note_to_int, int_to_note = create_note_mappings(note_dicts)

# Seed sequence
seed = [note['note'] for note in note_dicts[:sequence_length]]
pattern = [note_to_int[n] for n in seed]

# Sampling helper
def sample_with_temperature(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + 1e-8) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(preds), p=preds)

# Generate notes
generated = []
num_notes = 200
temperature = 0.8  # creativity control

for _ in range(num_notes):
    input_seq = np.reshape(pattern, (1, sequence_length))
    prediction = model.predict(input_seq, verbose=0)[0]
    index = sample_with_temperature(prediction, temperature)
    result = int_to_note[index]
    generated.append(result)

    pattern.append(index)
    pattern = pattern[1:]

# Create MIDI
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

for note in generated:
    note_int = int(note)
    velocity = random.randint(50, 100)
    track.append(Message('note_on', note=note_int, velocity=velocity, time=200))
    track.append(Message('note_off', note=note_int, velocity=0, time=100))

mid.save('generated_output.mid')
print("✅ Generated music saved as: generated_output.mid")
