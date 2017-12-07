from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
from keras.callbacks import ModelCheckpoint
import numpy as np
import random
import sys, re

# path = get_file('nietzsche.txt', origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
# text = open(path).read().lower()

# filename = 'data_parsed/drseuss.txt'
output_filename = 'output_text/shakespeare_words_out.txt'
# raw_text = open(filename, encoding='utf-8', errors='ignore').read().lower()

# load ascii text and covert to lowercase
filename = 'data_parsed/trump.txt'
raw_text = open(filename, encoding='utf8', errors='ignore').read()
raw_text = raw_text.lower()
# create mapping of unique chars to integers
wordList = re.sub("[^\w]", " ",  raw_text).split()
# print(len(wordList))
wordList = [w for w in wordList if re.match("^[a-z]*$", w)]
# print(len(wordList))
words = sorted(list(set(wordList)))
word_to_int = dict((w, i) for i, w in enumerate(words))

# text = text.lower()

print('corpus length:', len(raw_text))

# chars = sorted(list(set(text)))
print('total words:', len(words))
char_indices = dict((c, i) for i, c in enumerate(words))
indices_char = dict((i, c) for i, c in enumerate(words))

print(char_indices)

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 10
step = 3
sentences = []
next_chars = []
for i in range(0, len(wordList) - maxlen, step):
    sentences.append(wordList[i: i + maxlen])
    next_chars.append(wordList[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(words)), dtype=np.bool)
y = np.zeros((len(sentences), len(words)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


# build the model: a single LSTM
print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(words))))
# model.add(LSTM(128, input_shape=(maxlen, len(words)), return_sequences=True))
# model.add(LSTM(128, return_sequences=True))
# model.add(LSTM(128, return_sequences=True))
# model.add(LSTM(128))
model.add(Dense(len(words)))
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

filepath = 'weights-improvement-{epoch:02d}-{loss:.4f}-drseuss-words.hdf5'
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.fit(x, y,
          batch_size=128,
          epochs=30,
          callbacks=callbacks_list)

outfile = open(output_filename, 'w')
diversity = 0.5

start_index = random.randint(0, len(wordList) - maxlen - 1)
generated = ''
sentence = wordList[start_index: start_index + maxlen]
generated += sentence
print('----- Generating with seed: "' + sentence + '"')
sys.stdout.write(generated)
outfile.write(generated)

for i in range(500):
    x_pred = np.zeros((1, maxlen, len(words)))
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
