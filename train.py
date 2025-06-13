# train.py
from preprocess_notes import load_notes, prepare_sequences
from model import build_model

notes = load_notes('note_data.json')
X, y, vocab_size, encoder = prepare_sequences(notes)

model = build_model(vocab_size=vocab_size, seq_length=50)
model.summary()

model.fit(X, y, epochs=20, batch_size=64)

# Save model and encoder
model.save("note_lstm_model.h5")

import pickle
with open("note_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)
