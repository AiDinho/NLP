from nltk.corpus import brown
from nltk.probability import *

cfd = ConditionalFreqDist()
for sent in brown.tagged_sents():
    for word, tag in sent:
        if word =='run':
            cfd['run']/inc(tag)