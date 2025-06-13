import json
import numpy as np
import os
import subprocess
from keras.models import load_model
from mido import MidiFile, MidiTrack, Message
from tkinter import Tk, Label, Button, messagebox
from preprocess_notes import create_note_mappings

output_path = 'generated_output.mid'

def generate_music():
    label_status.config(text="🎵 Generating music...")

    model = load_model('note_lstm_model.h5')

    with open('note_data.json', 'r') as f:
        notes = json.load(f)

    sequence_length = 50
    note_dicts = notes if isinstance(notes[0], dict) else [{'note': n} for n in notes]
    note_to_int, int_to_note = create_note_mappings(note_dicts)

    seed = [note['note'] for note in note_dicts[:sequence_length]]
    pattern = [note_to_int[n] for n in seed]

    generated = []
    num_notes = 200

    for _ in range(num_notes):
        input_seq = np.reshape(pattern, (1, sequence_length))
        prediction = model.predict(input_seq, verbose=0)
        index = np.argmax(prediction)
        result = int_to_note[index]
        generated.append(result)
        pattern.append(index)
        pattern = pattern[1:]

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    for note in generated:
        track.append(Message('note_on', note=int(note), velocity=60, time=200))

    mid.save(output_path)
    label_status.config(text=f"✅ Music saved as: {output_path}")

def play_midi():
    if not os.path.exists(output_path):
        messagebox.showerror("Error", "Please generate music first.")
        return
    try:
        os.startfile(output_path)  # works on Windows
    except Exception as e:
        messagebox.showerror("Playback Error", str(e))

def open_folder():
    if not os.path.exists(output_path):
        messagebox.showerror("Error", "Please generate music first.")
        return
    folder_path = os.path.abspath(os.path.dirname(output_path))
    subprocess.Popen(f'explorer "{folder_path}"')

# --- UI Setup ---
root = Tk()
root.title("🎹 AI Music Generator")

label_title = Label(root, text="AI Music Generation", font=("Arial", 18))
label_title.pack(pady=10)

btn_generate = Button(root, text="🎼 Generate Music", command=generate_music, font=("Arial", 14))
btn_generate.pack(pady=10)

btn_play = Button(root, text="▶️ Play Generated MIDI", command=play_midi, font=("Arial", 12))
btn_play.pack(pady=5)

btn_open_folder = Button(root, text="📁 Open File Location", command=open_folder, font=("Arial", 12))
btn_open_folder.pack(pady=5)

label_status = Label(root, text="", font=("Arial", 12))
label_status.pack(pady=10)

root.mainloop()
