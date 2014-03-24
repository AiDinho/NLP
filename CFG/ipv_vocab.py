# Tagging and retagging the Vocab.gr

import nltk
from nltk.corpus import brown

#fvocab = open('Vocab.gr','r')           # the given Vocab.gr
fwords = open('./allowed_words.txt','r')
#fnew_vocab = open('./answer/Vocab.gr','w')  # the 'bettered" Vocab.gr
wsj = nltk.corpus.treebank.tagged_words()
wsjb = brown.tagged_words(categories='news')

cfd1 = nltk.ConditionalFreqDist(wsj)
cfd2 = nltk.ConditionalFreqDist((tag, word) for (word, tag) in wsj)

#for word in fwords:
#   word = word.rstrip()
word = '\'s'
print word, " ", cfd1[word].keys()

#for oldline in fvocab:
#   fnew_vocab.write(line)


#fvocab.close()
fwords.close()
#fnew_vocab.close()