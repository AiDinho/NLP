# Generate some improvements to the Vocab.gr

import nltk

try:
    fvocab_in = open("./Vocab.temp","r")
    fvocab_out = open("./Vocab_grail.gr","w")
except:
    print "Cannot open file."

print "...Generating..."
tagged_sents = []

for sent in nltk.corpus.webtext.sents('grail.txt'):
    tagged_sents = tagged_sents + nltk.pos_tag(sent)
    
#print tagged_sents
cfd = nltk.ConditionalFreqDist(tagged_sents)    
cfd_reverse = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_sents)

for line in fvocab_in:
    word = line.split()[2]
    keys = cfd[word].keys()
    if keys == []:
        fvocab_out.write("1    Misc    "+word+"\n")
    else:
        for key in keys:
            fvocab_out.write(str(cfd[word][key])+"    "+key+"    "+word+"\n")

print "...Finish!"
fvocab_in.close()
fvocab_out.close()