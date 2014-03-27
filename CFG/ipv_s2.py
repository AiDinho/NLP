# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 16:17:51 2014

@author: dif
"""
import nltk

fvocab = open("./Vocab_grail_no_weights.gr","r") 
fs2 = open("S2_grail.gr","w")

tagset = []
tagged_sents = []

print "...Generating..."

for line in fvocab:
    if line.startswith("\n") or line.startswith("#"):
        continue
    else:
        row = line.split()
        tagset.append(row[1])
tagset = list(set(tagset))

for i in range(len(tagset)):
    if tagset[i][0] == "_":
        continue
    fs2.write(str(1)+"    S2    _"+tagset[i]+"\n")

for i in range(len(tagset)):
    if tagset[i][0] == "_":
        continue
    for j in range(len(tagset)):
        if tagset[j][0] == "_":
            continue
        if i == j:
            fs2.write(str(1)+"    _"+tagset[i]+"    "+tagset[j]+"\n")
        else:
            fs2.write(str(1)+"    _"+tagset[i]+"    "+tagset[i]+"    _"+tagset[j]+"\n")


print "...Finish!"
'''
for sent in nltk.corpus.webtext.sents('grail.txt'):
    tagged_sents = tagged_sents + nltk.pos_tag(sent)
    
print tagged_sents
'''
    
fvocab.close()
fs2.close()