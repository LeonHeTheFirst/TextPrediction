import re


# function for parsing the data
def data_parser(text, dic):
    for i, j in dic.iteritems():
        text = re.sub(i, j, text)
    return text

# Params
max_chars = 500000

# Files to read and write to
input_file_name = '../data/shakespeare_raw.txt'
output_file_name = '../data_parsed/shakespeare.txt'

# Read file
input_file = open(input_file_name)
my_text = input_file.readlines()[:] # Read the whole text file,
input_file.close()

regexs = {'-':'',
    '\[(.*?)\]':'',
    '\[(.*?)':'',
    '(.*?)\]':'',
    '\((.*?)\)':'',
    '  +':' ',
    '^\t':'',
    '\t':' ',
    'SCENE.*':'',
    'ACT.*':'',
    '^[0-9].*':'', # Lines beginning with numeric char
    '.*\|.*':'', # Weird lines with | character
    '^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})\..*':'' # Roman Numerals
}

output_file = open(output_file_name, 'w')

num_chars = 0
for line in my_text:
    line = data_parser(line, regexs)

    if (line != '\n') and (num_chars < max_chars): # If line hasn't been reduced to empty line, write it out
        num_chars += len(line)
        output_file.write(line)

print("Parsed " + str(num_chars) + " characters from this file.")

output_file.close()



