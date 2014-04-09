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
import sys, math, random
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

def random_seq_sum(n, total):
    #Return a randomly chosen list of n positive integers summing to total.
    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
bitext_r = [[sentence.strip().split() for sentence in pair] for pair in zip(open(e_data),open(f_data))[:opts.num_sents]]

def train(bitext):
    tol = 1e-1  # the convergence tolerance, hand-tuned
    cutoff = 50 # the converged count cut-off, hand-tuned
    de = defaultdict(int)   # store the counts of words        
    df = defaultdict(int)   # in a hash table staying efficient
    english_words = set()
    foreign_words = set()
    for (f_sent, e_sent) in bitext:
        english_words.update(e_sent)
        foreign_words.update(f_sent)
    num = 0
    # use lambda to initialize the probability on the fly
    t_ef = defaultdict(lambda: float(1)/len(english_words)) 
    # precompute the training data for efficiency
    for (f_sent, e_sent) in bitext:
        for e_word in e_sent:
            de[num,e_word] += 1
        for f_word in f_sent:
            df[num,f_word] += 1
        num+=1
            # initialize the t_ef, uniformly by default
        for f_i in set(f_sent):
            for e_j in set(e_sent):
                t_ef[e_j, f_i] 

    pairs = t_ef.keys()
    num_probs = len(pairs)
    num_converged = 0

    while num_probs - num_converged > cutoff:
        num = 0    
        num_converged = 0
        c_ef = defaultdict(int)
        total_f = defaultdict(int)
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
            new_prob = c_ef[e,f]/total_f[f]
            delta = abs(t_ef[e,f] - new_prob)
            if delta < tol:
                num_converged += 1
            t_ef[e,f] = new_prob
    return t_ef

t_ef = train(bitext)   # gives the french to english alignments
t_fe = train(bitext_r) # gives the english to french alignments

# argmax part
penalty = 0.89


# store the reverse alignments in a reference list
a_ef = defaultdict()
num_sent = 0
for (f_sent, e_sent) in bitext_r:
    align_sent = []
    for (i, f) in enumerate(f_sent):
        a_max = 0
        for (j, e) in enumerate(e_sent):
            # add penalty to let the alighnment closer to the diagnal
            if t_fe[(e,f)]*pow(penalty, abs(i - j)) > a_max:
                a_max = t_fe[e,f]
                j_max = j
        align_sent.append((j_max, i))
    a_ef[num_sent] = align_sent
    num_sent += 1
    
# output the final alignments by referring to the reverse            
num_sent = 0    
for (f_sent, e_sent) in bitext:
    for (i, f) in enumerate(f_sent):
        a_max = 0
        for (j, e) in enumerate(e_sent):
            # add penalty to let the alighnment closer to the diagnal
            if t_ef[(e,f)]*pow(penalty, abs(i - j)) > a_max:
                a_max = t_ef[e,f]
                j_max = j
        # here, only those alignments also appear on the reverse order get output 
        if((i,j_max) in a_ef[num_sent]):
            sys.stdout.write("%i-%i " % (i,j_max))
    sys.stdout.write("\n")
    num_sent += 1
