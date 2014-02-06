# plots dispersion of word occurences in
# Sense and Sensibility by Jane Austen

from nltk.corpus import gutenberg
from nltk.draw import dispersion_plot
from nltk import stem
p = stem.PorterStemmer()
text = gutenberg.words('austen-sense.txt')
words = ['walking','talking','hunting']
vocab = set(text) #build a vocabulary
for word in vocab:
    if p.stem(word) == 'walk' or p.stem(word) == 'talk' or p.stem(word) =='hunt':
        words.append(word)
dispersion_plot(gutenberg.words('austen-sense.txt'), words)
