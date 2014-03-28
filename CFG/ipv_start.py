# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 22:44:54 2014
This module is used to improve the start transitions
@author: Silvery Fu
"""
import nltk

fvocab = open("./Vocab.gr","r") 
fs = open("./Start.gr","w")

print "...Generating..."

def addprefix(word):
    if word == "." or word == "," or word == ":":
        return "$"+word
    else:
        return word

tagged_sents_penn = nltk.corpus.treebank.tagged_sents()

start_tag = []

for sent in tagged_sents_penn:
    start_tag.append(sent[0][1])

fd = nltk.FreqDist(start_tag)

tagset = []

for line in fvocab:
    if line.startswith("\n") or line.startswith("#"):
        continue
    else:
        row = line.split()
        tagset.append(row[1])
tagset = list(set(tagset))

for tag in tagset:
    if tag[0] == ("_"):
        continue
    tag = tag.rstrip("_t").lstrip("$")
    fs.write(str(1+(1+fd[tag])/10)+"    S2    _"+tag+"_t\n")

print "...Finish!"

fvocab.close()
fs.close()


