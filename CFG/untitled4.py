# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 09:25:05 2014

@author: dif
"""
import nltk

for sent in nltk.corpus.webtext.sents('grail.txt'):
    tagged_sents = tagged_sents + nltk.pos_tag(sent)
print tagged_sents
wsj = nltk.corpus.treebank.tagged_words()    
#print tagged_sents
cfd = nltk.ConditionalFreqDist(tagged_sents)    
cfd_reverse = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_sents)

cfd1 = nltk.ConditionalFreqDist(wsj)

#for sent in nltk.corpus.webtext.sents('grail.txt'):
#    print sent
print cfd1['quest'].keys()

