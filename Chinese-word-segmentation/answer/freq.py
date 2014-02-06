import nltk
from nltk.probability import FreqDist

sense = nltk.corpus.gutenberg.words('austen-sense.txt')
fdist = FreqDist(sense)
rank = 0
for item in fdist.items():
    rank = rank + 1  
    result= str(rank)+" "+str(item[1])+" "+str(item[0])
    print result
