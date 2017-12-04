from textstat.textstat import textstat
import os
import matplotlib.pyplot as plt
# import nltk
import enchant
import string
# string.punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


# Directories for data input/output
input_dir_name = '../output_text/drseuss_multilayer'
output_dir_name = '../text_performance/drseuss_multilayer'

# US dictionary for checking
d = enchant.Dict("en_US")

# Make output directory
if not os.path.exists(output_dir_name):
    os.makedirs(output_dir_name)

# Find all outputs in directory
files = []
epochs = []
for file in os.listdir(input_dir_name):
    if file.endswith(".txt"):
        epoch_str = file[-6:-4]  # Get epoch number
        # print(epoch_str)
        if epoch_str.isdigit():
            files.append(file)
            epochs.append(int(epoch_str))
            # print(int(epoch_str))

# Evaluate performance of each sample
flesch_reading_ease = [None]*len(files)
smog_index = [None]*len(files)
flesch_kincaid_grade = [None]*len(files)
coleman_liau_index = [None]*len(files)
automated_readability_index = [None]*len(files)
dale_chall_readability_score = [None]*len(files)
difficult_words = [None]*len(files)
linsear_write_formula = [None]*len(files)
gunning_fog = [None]*len(files)
text_standard = [None]*len(files)
percent_words = [None]*len(files)
num_words = [None]*len(files)
fig = [None]*(len(files)+1)
for i in range(0, len(files)):
    file = files[i]
    epoch = epochs[i]-1
    print(file)
    with open(os.path.join(input_dir_name, file), 'r') as myfile:
        test_data = myfile.read().replace('\n', '')
        # print(len(test_data))
        # print(epoch)
        # print(len(files))
        flesch_reading_ease[i] = textstat.flesch_reading_ease(test_data)
        smog_index[i] = textstat.smog_index(test_data)
        flesch_kincaid_grade[i] = textstat.flesch_kincaid_grade(test_data)
        coleman_liau_index[i] = textstat.coleman_liau_index(test_data)
        automated_readability_index[i] = textstat.automated_readability_index(test_data)
        dale_chall_readability_score[i] = textstat.dale_chall_readability_score(test_data)
        difficult_words[i] = textstat.difficult_words(test_data)
        linsear_write_formula[i] = textstat.linsear_write_formula(test_data)
        gunning_fog[i] = textstat.gunning_fog(test_data)
        text_standard[i] = textstat.text_standard(test_data)

        num_true_words = 0
        words = test_data.split()
        for word in words:
            word_stripped = word.strip(string.punctuation).lower()
            # print(word_stripped)
            if word_stripped:
                # print(d.check(word_stripped))
                if d.check(word_stripped):
                    num_true_words += 1
        percent_words[i] = num_true_words / float(len(words))
        num_words[i] = len(words)

print(epochs)
# print "flesch_reading_ease: " + str(flesch_reading_ease)
# print "smog_index: " + str(smog_index)
# print "flesch_kincaid_grade: " + str(flesch_kincaid_grade)
# print "coleman_liau_index: " + str(coleman_liau_index)
# print "automated_readability_index: " + str(automated_readability_index)
# print "dale_chall_readability_score: " + str(dale_chall_readability_score)
# print "difficult_words: " + str(difficult_words)
# print "linsear_write_formula: " + str(linsear_write_formula)
# print "gunning_fog: " + str(gunning_fog)
# print "text_standard: " + str(text_standard)
# print "percent_words: " + str(percent_words)

plt.close("all")

titles = []

idx = 0
fig[idx] = plt.figure(idx)
titles.append('flesch_reading_ease')
plt.plot(epochs, flesch_reading_ease, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('smog_index')
plt.plot(epochs, smog_index, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('flesch_kincaid_grade')
plt.plot(epochs, flesch_kincaid_grade, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('coleman_liau_index')
plt.plot(epochs, coleman_liau_index, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('automated_readability_index')
plt.plot(epochs, automated_readability_index, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('dale_chall_readability_score')
plt.plot(epochs, dale_chall_readability_score, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('difficult_words')
plt.plot(epochs, difficult_words, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('linsear_write_formula')
plt.plot(epochs, linsear_write_formula, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('gunning_fog')
plt.plot(epochs, gunning_fog, 'ro')
plt.title(titles[-1])
plt.grid(True)
# # plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('percent_words')
plt.plot(epochs, percent_words, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

fig[idx] = plt.figure(idx)
titles.append('num_words')
plt.plot(epochs, num_words, 'ro')
plt.title(titles[-1])
plt.grid(True)
# plt.show()
idx += 1

# fig[idx] = plt.figure(idx)
# plt.plot(num_words, percent_words, 'ro')
# plt.title('num_words vs percent_words')
# plt.grid(True)
# # plt.show()
# idx += 1


# Notes:
# Positive corr with
#   flesch_reading_ease
#   coleman_liau_index


for i in range(0, idx):
    plt.figure(i)
    plt.savefig(os.path.join(output_dir_name, titles[i] + '.png'), bbox_inches='tight')
# plt.figure(11)
# plt.savefig(os.path.join(output_dir_name, 'num_words.png'), bbox_inches='tight')
# plt.savefig(os.path.join(output_dir_name, 'percent_words.png'), bbox_inches='tight')


# plt.show()
