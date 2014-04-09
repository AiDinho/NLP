#!/usr/bin/env python
"""
    python align.py [options]

    options are:

	-p DIR/PREFIX   prefix for parallel data, Defaults: DIR=../ PREFIX=../hansards when running from answer directory
	-n NUMBER       number of training examples to use, Default: n = sys.maxint

    This program implements IBM Model 1 in EM algorithm, with improvements:
    - 1. Gives penalty to those pairs who are away from each other in word distance
    - 2. bidirectionally aligned corpora e -> f, f -> e and take intersection of the alignment points
    - 3. Optionally use heuristic to grow additional alignment points
    - 4. Can generate random starting distribution
    - 5. Add alignments from foreign words to Null and delete them
    - 6. Use some precomputed hash tables to improve efficiency
    Given 10,000 bitext sentences, it can give Precision = 0.920570; Recall = 0.621302; AER = 0.243902 (without using heuristics)
    Given 100,000 bitext sentences, it can give Precision = 0.928571; Recall = 0.653846; AER = 0.218354 (without using heuristics)
"""
from __future__ import division
from collections import defaultdict
import optparse
import sys, random
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

# train an IBM Model 1 given the bitext
def train(bitext, _tol, _cutoff):
    tol = _tol              # the convergence tolerance, use hand-tuned input
    cutoff = _cutoff        # the converged count cut-off, use hand-tuned
    de = defaultdict(int)   # store the counts of words        
    df = defaultdict(int)   # in a hash table staying efficient
    english_words = set()
    foreign_words = set()
    for (f_sent, e_sent) in bitext:
        english_words.update(e_sent)
        foreign_words.update(f_sent)
    english_words.add('nil')
    # use lambda to initialize the probability on the fly
    default_prob = float(1)/len(english_words)
    t_ef = defaultdict(lambda: default_prob) 
    num = 0
    # precompute the training data for efficiency
    for (f_sent, e_sent) in bitext:
        for e_word in e_sent+['nil']:
            de[num,e_word] += 1
        for f_word in f_sent:  # add Null alignments here
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
            e_words = list(set(e_sent))     
            f_words = list(set(f_sent))
            for e_word in e_words+['nil']:
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

t_ef = train(bitext, 1e-1, 50)   # gives the french to english alignments
t_fe = train(bitext_r, 1e-1, 50) # gives the english to french alignments

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
                if e == 'nil':
                    j_max = -1
                else:
                    j_max = j
        align_sent.append((j_max, i))
    a_ef[num_sent] = align_sent
    num_sent += 1
    
# output the final alignments by referring to the reverse            
num_sent = 0
cut_off_heuristic = 1e-1 # the cutoff probability for the prob of the candidates given by heuristc     
for (f_sent, e_sent) in bitext:
    curr_j = 0
    for (i, f) in enumerate(f_sent):
        a_max = 0
        prev_j = curr_j
        for (j, e) in enumerate(e_sent):
            # add penalty to let the alighnment closer to the diagnal
            if t_ef[(e,f)]*pow(penalty, abs(i - j)) > a_max:
                a_max = t_ef[e,f]
                if e == 'nil':
                    j_max = -1
                else:
                    j_max = j
        # here, only those alignments also appear on the reverse order get output 
        if((i,j_max) in a_ef[num_sent]) and j_max != -1:
            curr_j = j_max            
            sys.stdout.write("%i-%i " % (i,j_max))
        # use a heuristic here, but does not always work well, since 
        # it depends on the languages and corpus
        else:
            if prev_j + 1 < len(e_sent):
                curr_j = prev_j + 1
                ''' # more complicated heuristics                
                cand = [-1,-2,0,1,2] # the candidate positions for the "alignee"          
                p_max = 0                
                for c in cand:
                    if prev_j + c >= 0 and (t_ef[e_sent[prev_j+c],f] > p_max):
                        p_max = t_ef[e_sent[prev_j+c],f]
                        curr_j = prev_j + c
                '''
                # only those trustworthy enough get selected
                if t_ef[e_sent[curr_j],f] >= cut_off_heuristic:
                    sys.stdout.write("%i-%i " % (i,curr_j))
    sys.stdout.write("\n")
    num_sent += 1