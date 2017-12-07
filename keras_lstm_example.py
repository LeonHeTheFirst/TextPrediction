'''Example script to generate text from Nietzsche's writings.

At least 20 epochs are required before the generated text
starts sounding coherent.

It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.

If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
from keras.callbacks import ModelCheckpoint
import numpy as np
import random
import sys

# path = get_file('nietzsche.txt', origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
# text = open(path).read().lower()

filename = 'data_parsed/clinton.txt'
output_filename = 'output_text/trump_out_long.txt'
text = open(filename, encoding='utf-8', errors='ignore').read().lower()
# text = text.lower()

print('corpus length:', len(text))

chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

print(char_indices)

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars))))
# model.add(LSTM(128, input_shape=(maxlen, len(chars)), return_sequences=True))
# model.add(LSTM(128, return_sequences=True))
# model.add(LSTM(128, return_sequences=True))
# model.add(LSTM(128))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))


optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


print('-' * 50)

filepath = 'weights-improvement-{epoch:02d}-{loss:.4f}-trump-100c.hdf5'
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.fit(x, y,
          batch_size=128,
          epochs=30,
          callbacks=callbacks_list)

outfile = open(output_filename, 'w')
diversity = 0.5

start_index = random.randint(0, len(text) - maxlen - 1)
generated = ''
sentence = text[start_index: start_index + maxlen]
generated += sentence
print('----- Generating with seed: "' + sentence + '"')
sys.stdout.write(generated)
outfile.write(generated)

for i in range(500):
    x_pred = np.zeros((1, maxlen, len(chars)))
    for t, char in enumerate(sentence):
        x_pred[0, t, char_indices[char]] = 1.

    preds = model.predict(x_pred, verbose=0)[0]
    next_index = sample(preds, diversity)
    next_char = indices_char[next_index]

    generated += next_char
    sentence = sentence[1:] + next_char

    sys.stdout.write(next_char)
    outfile.write(next_char)
print()

# # train the model, output generated text after each iteration
# for iteration in range(1, 5):
#     print()
#     print('-' * 50)

#     start_index = random.randint(0, len(text) - maxlen - 1)

#     for diversity in [0.2, 0.5, 1.0]:
#         print()
#         print('----- diversity:', diversity)

#         generated = ''
#         sentence = text[start_index: start_index + maxlen]
#         generated += sentence
#         print('----- Generating with seed: "' + sentence + '"')
#         sys.stdout.write(generated)
#         outfile.write(generated)

#         for i in range(400):
#             x_pred = np.zeros((1, maxlen, len(chars)))
#             for t, char in enumerate(sentence):
#                 x_pred[0, t, char_indices[char]] = 1.

#             preds = model.predict(x_pred, verbose=0)[0]
#             next_index = sample(preds, diversity)
#             next_char = indices_char[next_index]

#             generated += next_char
#             sentence = sentence[1:] + next_char

#             sys.stdout.write(next_char)
#             outfile.write(next_char)
#         print()