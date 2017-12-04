from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
from keras.callbacks import ModelCheckpoint
import numpy as np
import random
import sys, re, os

filename = 'data_parsed/trump.txt'
output_filename = 'output_text/trump_out_epoch_1.txt'
weight_dir_name = 'weights/trump/words/'
weights_filename = 'weights/trump/weights-improvement-01-1.9294-trump-larger.hdf5'
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

# print(char_indices)

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 10
step = 3
sentences = []
next_words = []
for i in range(0, len(wordList) - maxlen, step):
    sentences.append(wordList[i: i + maxlen])
    next_words.append(wordList[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(words)), dtype=np.bool)
y = np.zeros((len(sentences), len(words)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_words[i]]] = 1


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
# model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

print('-' * 50)

files = []
for file in os.listdir(weight_dir_name):
    if file.endswith(".hdf5"):
        files.append(file)

# outfile = open(output_filename, 'w')
diversity = 0.5

start_index = random.randint(0, len(wordList) - maxlen - 1)
generated = ''
sentence = wordList[start_index: start_index + maxlen]
for word in sentence:
	generated += word + ' '
print('----- Generating with seed: "' + ' '.join(word for word in sentence) + '"')
sys.stdout.write(generated)
# outfile.write(generated)

for weight_file in files:

    model.load_weights(weight_dir_name + weight_file)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    weight_file.replace('.', '-')
    substrings = weight_file.split('-')
    epoch_number = substrings[2]
    source = substrings[4]
    new_output_filename = 'output_text/' + 'trump' + '_epoch_' + epoch_number + '.txt'
    new_output_file = open(new_output_filename, 'w')

    for i in range(1000):
        x_pred = np.zeros((1, maxlen, len(words)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_word = indices_char[next_index]

        generated += next_word
        sentence = sentence[1:] + [next_word]

        sys.stdout.write(next_word + ' ')
        new_output_file.write(next_word + ' ')
    print()
    new_output_file.close()