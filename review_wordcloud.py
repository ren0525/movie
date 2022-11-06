import re
import sys
import matplotlib.pyplot as plt
import spacy
import wordcloud

movie_name = 'godzila'

input_fn = 'text/review.txt'

include_pos = ('NOUN', 'VERB', 'ADJ')
stopwords = ('する', 'ある', 'ない', 'いう', 'もの', 'こと', 'よう', 'なる', 'ほう')

nlp = spacy.load("ja_ginza")

with open(input_fn, 'r') as f:
    text = f.read()

doc = nlp(text)
words = [token.lemma_ for token in doc
         if token.pos_ in include_pos and token.lemma_ not in stopwords]

wc = wordcloud.WordCloud(
    background_color='white',
    font_path='/mnt/c/Windows/Fonts/msgothic.ttc',
    max_font_size=100)
img = wc.generate(' '.join(words))

plt.figure(figsize=(8, 4))
plt.imshow(img, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig(f'photo/{movie_name}.png')