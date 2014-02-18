from nltk.corpus import wordnet
import sys

if __name__=="__main__":
    if(len(sys.argv)>1):    
        synsets = wordnet.synsets(sys.argv[1])
        for synset in synsets:
            print "######################################################"
            print "Name:", synset.name
            print "Definition:", synset.definition
            for example in synset.examples:
                print "Example:", example
            print "######################################################"