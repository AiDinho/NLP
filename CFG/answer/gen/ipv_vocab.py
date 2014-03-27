# Generate some improvements to the Vocab.gr

import nltk

try:
    fvocab_in = open("./Vocab.gr", "r")# notice, this file has been modified to fit the penn tag sets
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
    if line.startswith("#") or line.startswith("\n"):
        fvocab_out.write(line)        
        continue
    else:
        row = line.split()        
        count = row[0]        
        tag = row[1]        
        word = row[2]
        rest = ""
        if len(row) > 3:
            rest = row[3]
        
        if tag == "Misc":
            keys = cfd[word].keys()
            if keys == []:
                fvocab_out.write("1    Misc    "+word+"    "+rest+"\n")
            else:
                for key in keys:
                    fvocab_out.write(str(cfd[word][key])+"    "+key+"    "+word+"    "+rest+"\n") #TODO Hand tune the weights
        else:
            fvocab_out.write(str(1+cfd_reverse[tag][word])+"    "+tag+"    "+word+"    "+rest+"\n")
            
print "...Finish!"
fvocab_in.close()
fvocab_out.close()