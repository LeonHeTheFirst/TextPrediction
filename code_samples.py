# read in input text file, filtering out unknown characters and converting to lowercase
text = open(filename, encoding='utf-8', errors='ignore').read().lower()

# enumerate vocabulary (character set) as integers
chars = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# create overlapping sequences of characters
maxlen = 40 # length of sequence
step = 3 # amount to increment for each sequence
sequences = [] # "input" sequence
next_chars = [] # "output" character
for i in range(0, len(text) - maxlen, step):
    sequences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])

# convert the sequences into numpy matrices
# input characters are one-hot encoded
x = np.zeros((len(sequences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sequences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sequences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1



# build the model, which will be sequential layers
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars)))) # input layer with matrix input
model.add(Dense(len(chars))) # output layer
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01) # found to perform better than gradient descent
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

# file template for saving weights after each epoch
filepath = 'weights-improvement-{epoch:02d}-{loss:.4f}-textsource.hdf5'
# don't save weights if loss increases in an epoch
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

# train network on x and y for 30 epochs, updating every 128 data pieces
model.fit(x, y, batch_size=128, epochs=30, callbacks=callbacks_list)


# 4 LSTM layers
model.add(LSTM(128, input_shape=(maxlen, len(chars)), return_sequences=True))
model.add(LSTM(128, return_sequences=True))
model.add(LSTM(128, return_sequences=True))
model.add(LSTM(128))



# randomly select a seed string of length maxlen from source text
start_index = random.randint(0, len(text) - maxlen - 1)
sentence = text[start_index: start_index + maxlen]
print('Seed: "' + sentence + '"')
sys.stdout.write(sentence)

# generate 1000 characters of new text with trained network
diversity = 0.5 # temperature to use when selecting next character
for i in range(1000):
	# matrix to use for inputting to network
    x_pred = np.zeros((1, maxlen, len(chars)))
    # set one-hot encoding in matrix
    for t, char in enumerate(sentence):
        x_pred[0, t, char_indices[char]] = 1.
    # infer probabilities for next character
    preds = model.predict(x_pred, verbose=0)[0]
    # find index of next character in dictionary based on
    # probability distribution and temperature
    next_index = sample(preds, diversity)
    # get next character
    next_char = indices_char[next_index]
    # update input string
    sentence = sentence[1:] + next_char

    sys.stdout.write(next_char)

def sample(preds, temperature):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)