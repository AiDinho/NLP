from nltk.corpus import cmudict
import sys
transcr = cmudict.dict() # warning: this can be very slow
print >>sys.stderr, "cmudict loaded ..."
for line in sys.stdin:
    words = line.split()
    for word in words:
        if word in transcr:
            print transcr[word]
        else:
            print >>sys.stderr, "could not find", word
