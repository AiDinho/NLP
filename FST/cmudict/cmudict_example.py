from nltk.corpus import cmudict
for word, pron in cmudict.entries():
    if (pron[-4:] == ['P', 'IH0', 'K', 'S']):
        print word.lower(),
print
transcr = cmudict.dict() # warning: this can be very slow
print transcr['herbalists']
