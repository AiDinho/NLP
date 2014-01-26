# plots dispersion of word occurences in
# Sense and Sensibility by Jane Austen

from nltk.corpus import gutenberg
from nltk.draw import dispersion_plot
words = ['Elinor', 'Marianne', 'Edward', 'Willoughby']
dispersion_plot(gutenberg.words('austen-sense.txt'), words)
