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
import sys, math
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
tol = pow(10,-4)  # the convergence tolerance
de = defaultdict(int)   # store the counts of words        
df = defaultdict(int)   # in a hash table staying efficient
num = 0
# permutate all the combinations of f -> e
for (f_sent, e_sent) in bitext:
    for e_word in e_sent:
        de[num,e_word] += 1
    for f_word in f_sent:
        df[num,f_word] += 1
    num+=1
    for f_i in set(f_sent):
        for e_j in set(e_sent):
            t_ef[e_j, f_i] = 1

pairs = t_ef.keys()
l = len(pairs)
# initialize the t_ef, uniformly by default
for (e, f) in t_ef.keys():
    t_ef[e, f] = 1/l

curr_L = 0
prev_L = tol + 1

for i in range(5):
    prev_L = curr_L
    curr_L = 0
    num = 0    
    for (e, f) in pairs:
        c_ef[e,f] = 0 
        total_f[f] = 0
    for (f_sent, e_sent) in bitext:
        e_words = set(e_sent)     
        f_words = set(f_sent)
        for e_word in e_words:
            n_e = de[num, e_word]
            total = 0
            for f_word in f_words:
                total += t_ef[e_word,f_word]*n_e
            for f_word in f_words:
                n_f = df[num, f_word]
                rhs = t_ef[e_word,f_word]*n_e*n_f/total
                c_ef[e_word,f_word] += rhs
                total_f[f_word] += rhs
        num+=1
    for (e, f) in pairs:
        t_ef[e,f] = c_ef[e,f]/total_f[f]
        curr_L += math.log(t_ef[e,f],2)
    print curr_L


'''
for (f_sent, e_sent) in bitext:
    for (i, f) in enumerate(f_sent):
        a_max = 0
        for (j, e) in enumerate(e_sent):
            if t_ef[(e,f)] > a_max:
                a_max = t_ef[e,f]
                j_max = j
        sys.stdout.write("%i-%i " % (i,j_max))
    sys.stdout.write("\n")  
                
'''
