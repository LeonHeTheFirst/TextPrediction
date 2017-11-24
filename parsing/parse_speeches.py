import re
import os
import io
import unicodedata
import codecs

# function for parsing the data
def data_parser(text, dic):
    for i, j in dic.iteritems():
        text = re.sub(i, j, text)
    return text

# Params
max_chars = 500000

# Directory with files to read and write to
input_dir_name = '../data/speeches/trump'
#input_dir_name = '../data/speeches/clinton'
output_file_name = '../data_parsed/trump.txt'
#output_file_name = '../data_parsed/clinton.txt'

regexs = {'-':'',
    '\[(.*?)\]':'', # Remove characters in brackets
    '\((.*?)\)':'', # Remove characters in parans
    '  +':' ', # Remove extra spaces
    '^\t':'', # Remove tabs at beginning on line
    '\t':' ', # Change Tabs to spaces
    '^[0-9].*':'', # Lines beginning with numeric char
    '.*\|.*':'', # Weird lines with | character
    '^Audience.*':'', # Remove audience lines
    '^Trump: ':'', # Remove trump labels
    '^QUESTION:.* ':'',
    '^CLINTON: ':'',
    '^KINHAN:.*':'',
    '^MICHAEL FEEL:.*':'',
    '^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\..*':'' # Roman Numerals
}


files = []
for file in os.listdir(input_dir_name):
    if file.endswith(".txt"):
        files.append(file)


output_file = open(output_file_name, 'w')

num_chars = 0
for input_file_name in files:
    # Read file
    input_file = open(os.path.join(input_dir_name, input_file_name))
    my_text = input_file.readlines()[:] # Read the whole text file,
    #my_text = codecs.open(os.path.join(input_dir_name, input_file_name), 'r', encoding='utf-8').readlines()
    input_file.close()

    for line in my_text:
        line = data_parser(line, regexs)

        if (line != '\n') and (line != '\r\n') and (num_chars < max_chars): # If line hasn't been reduced to empty line, write it out
            num_chars += len(line)
            output_file.write(line)

output_file.close()

print("Parsed " + str(num_chars) + " characters from this file.")

