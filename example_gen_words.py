# Load LSTM network and generate text
import sys
import numpy
import re
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import Dropout
# from keras.layers import LSTM
# from keras.callbacks import ModelCheckpoint
# from keras.utils import np_utils

# load ascii text and covert to lowercase
filename = 'parsing/shakespeare.txt'
raw_text = open(filename, encoding='utf8').read()
raw_text = raw_text.lower()

# create mapping of unique chars to integers
wordList = re.sub("[^\w]", " ",  raw_text).split()
# print(len(wordList))
wordList = [w for w in wordList if re.match("^[a-z]*$", w)]

# create mapping of unique chars to integers, and a reverse mapping
words = sorted(list(set(wordList)))
word_to_int = dict((w, i) for i, w in enumerate(words))
int_to_word = dict((i, w) for i, w in enumerate(words))
# summarize the loaded data
n_words = len(wordList)
n_vocab = len(words)
print('Total Words: ', n_words)
print('Total Vocab: ', n_vocab)

# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_words - seq_length, 1):
	seq_in = wordList[i:i + seq_length]
	seq_out = wordList[i + seq_length]
	dataX.append([word_to_int[word] for word in seq_in])
	dataY.append(word_to_int[seq_out])
n_patterns = len(dataX)
print('Total Patterns: ', n_patterns)
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)


# one hot encode the output variable
y = np_utils.to_categorical(dataY)
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
# load the network weights
filename = 'weights-improvement-20-2.0762-larger.hdf5'
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')
# pick a random seed
start = numpy.random.randint(0, len(dataX)-1)
pattern = dataX[start]
print('Seed:')
outstring = ('\'' + ''.join([int_to_word[value] for value in pattern]) + '\'').encode('utf-8')
print(outstring)
# generate words
for i in range(1000):
	x = numpy.reshape(pattern, (1, len(pattern), 1))
	x = x / float(n_vocab)
	prediction = model.predict(x, verbose=0)
	index = numpy.argmax(prediction)
	result = int_to_word[index]
	seq_in = [int_to_word[value] for value in pattern]
	print(result.encode('utf-8').decode('utf-8'), end='')
	pattern.append(index)
	pattern = pattern[1:len(pattern)]
print('\nDone.')