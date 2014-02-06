from nltk.corpus import cmudict
transcr = cmudict.dict() # warning: this can be very slow
i = 1
for entry in transcr['ajito']:
  print "ajito %d %s" % (i, " ".join(entry))
  i += 1
