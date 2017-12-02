from os import path
from wordcloud import WordCloud


# Directory with files to read and write to
input_dir_name = '../data_parsed/trump.txt'
input_dir_name = '../data_parsed/clinton.txt'
input_dir_name = '../data_parsed/shakespeare.txt'
input_dir_name = '../data_parsed/drseuss.txt'
output_file_name = '../wordclouds/trump.png'
output_file_name = '../wordclouds/clinton.png'
output_file_name = '../wordclouds/shakespeare.png'
output_file_name = '../wordclouds/drseuss.png'

# Read the whole text.
text = open(input_dir_name).read()

# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
fig = plt.figure(frameon=False)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
# plt.show()

wordcloud.to_file(output_file_name)


# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()

# plt.savefig(output_file_name)


