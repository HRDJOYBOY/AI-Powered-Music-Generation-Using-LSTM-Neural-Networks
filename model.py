# model.py
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding

def build_model(vocab_size, seq_length):
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=100, input_shape=(seq_length,)))
    model.add(LSTM(128, return_sequences=False))
    model.add(Dense(vocab_size, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
