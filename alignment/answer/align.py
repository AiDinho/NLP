#!/usr/bin/env python
"""
    python align.py [options]

    options are:

	-p DIR/PREFIX   prefix for parallel data, Defaults: DIR=../ PREFIX=../hansards when running from answer directory
	-n NUMBER       number of training examples to use, Default: n = sys.maxint
"""
from __future__ import division
from collections import defaultdict
import optparse
import sys
import os.path

optparser = optparse.OptionParser()
optparser.add_option("-p", "--data", dest="train", default="data/hansards", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="e", help="Suffix of English filename (default=e)")
optparser.add_option("-f", "--french", dest="french", default="f", help="Suffix of French filename (default=f)")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.french)
e_data = "%s.%s" % (opts.train, opts.english)

if not ( os.path.isfile(f_data) and os.path.isfile(e_data) ):
    print >>sys.stderr, __doc__.strip('\n\r')
    sys.exit(1)

sys.stderr.write("Training with IBM Model 1...")
bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]

t_ef = defaultdict(float)
c_ef = defaultdict(int)
total_f = defaultdict(int)
e_words = []
f_words = []
# permutate all the combinations of f -> e
for (n, (f, e)) in enumerate(bitext):
    for f_i in set(f):
        f_words.append(f_i)
        for e_j in set(e):
            e_words.append(e_j)
            t_ef[(e_j, f_i)] = 1

e_words = list(set(e_words))
f_words = list(set(f_words))

pairs = t_ef.keys()
l = len(pairs)
# initialize the t_ef, uniformly by default
for (e, f) in t_ef.keys():
    t_ef[(e, f)] = 1/l

for (e, f) in pairs:
    c_ef[(e,f)] = 0
    total_f[f] = 0
    for (n, (f_sent, e_sent)) in enumerate(bitext):
        for e_word in set(e_sent):
            total = 0
