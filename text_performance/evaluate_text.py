from textstat.textstat import textstat


# input_file_names = ['../output_text/clinton_out.txt',
input_file_names = ['../output_text/trump_out.txt',
                    '../output_text/shakespeare_out.txt',
                    '../output_text/drseuss_out.txt']

# input_file_names = ['../data_parsed/trump.txt',
input_file_names = ['../data_parsed/shakespeare.txt',
                    '../data_parsed/drseuss.txt']

for i in range(0, len(input_file_names)):
    input_file_name = input_file_names[i]
    print(input_file_name)
    with open(input_file_name, 'r') as myfile:
        test_data = myfile.read().replace('\n', '')

    print "flesch_reading_ease: " + str(textstat.flesch_reading_ease(test_data))
    print "smog_index: " + str(textstat.smog_index(test_data))
    print "flesch_kincaid_grade: " + str(textstat.flesch_kincaid_grade(test_data))
    print "coleman_liau_index: " + str(textstat.coleman_liau_index(test_data))
    print "automated_readability_index: " + str(textstat.automated_readability_index(test_data))
    print "dale_chall_readability_score: " + str(textstat.dale_chall_readability_score(test_data))
    print "difficult_words: " + str(textstat.difficult_words(test_data))
    print "linsear_write_formula: " + str(textstat.linsear_write_formula(test_data))
    print "gunning_fog: " + str(textstat.gunning_fog(test_data))
    print "text_standard: " + str(textstat.text_standard(test_data))


