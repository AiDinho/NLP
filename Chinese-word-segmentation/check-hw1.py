"""
Here each group tests single python program which must be named with the group name plus a .py suffix. These programs are executed with the same python interpreter used to run the check program.

a = system output
b = reference output
"""

from __future__ import division
import check
import sys, os, codecs, re
import difflib
import nltk

def edgews_normalize(*parts):
    def filter(x):
        x = [l.strip() for l in x]
        return [l + '\n' for l in x if l != '']
    return [filter(x) for x in parts]

def sepws_normalize(*parts):
    return [[re.sub("[         \v]+", " ", l) for l in x] for x in parts]

def diff_almost_exact(a, b, output):
    a, b = edgews_normalize(a, b)
    if a != b:
            output.write("Diff in output:\n")
            output.writelines(difflib.unified_diff(a, b))
            return False
    return True

def diff_unordered(a, b, output):
    a, b = edgews_normalize(a, b)
    a, b = sorted(a), sorted(b)
    if a != b:
            output.write("Diff in sorted output:\n")
            output.writelines(difflib.unified_diff(a, b))
            return False
    return True

def diff_freqs(a, b, output):
    a, b = edgews_normalize(a, b)
    a, b = sepws_normalize(a, b)
    ranks_a, ranks_b = [[l[:l.find(' ') or None] + '\n' for l in x] for x in [a, b]]
    freqs_a, freqs_b = [sorted(l[(l.find(' ') or 0)+1:] for l in x) if len(l) > 1 else [] for x in [a, b]]
    if not (ranks_a == ranks_b and freqs_a == freqs_b):
            output.write("Diff in sorted rank numbers:\n")
            output.writelines(difflib.unified_diff(ranks_a, ranks_b))
            output.write("Diff in sorted frequencies:\n")
            output.writelines(difflib.unified_diff(freqs_a, freqs_b))
            return False
    return True

def segment_bitstring(a):
    """
    this function is deprecated. 
    it was originally used to compute word segmentation accuracy.
    it was replaced by nltk.metrics.scores.f_measure()
    """
    a = a.strip()
    a = a[1:]
    a += ' ' # add a space at the end for the last char
    bitstring = '0'
    for i in a:
        if i == ' ':
            bitstring += '1'
        else:
            bitstring += '0'
    return bitstring

def print_fmeasure(a, b, output):
    """
    assumes that the input lines are in UTF-8
    used to compute f-measure for Chinese word segmentation
    sys.stdout is temporarily changed to enable debugging of UTF-8
    """
    old = sys.stdout
    sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
    score = 0
    for i in range(len(a)):
        output_utf8 = set(unicode(a[i], 'utf-8').split())
        gold_utf8 = set(unicode(b[i], 'utf-8').split())
        score += nltk.metrics.scores.f_measure(gold_utf8, output_utf8)
    print "Score: %.2f" % ((score/len(a))*100)
    output.write("Score: %.2f" % ((score/len(a))*100))
    sys.stdout = old
    return True

def make_file_exists(filename):
    def diff_exists(a, b, output):
        return True
    def make_check(**args):
        gold_path = os.path.join(args['testcases_path'], args['group'], filename)
        return { 'gold': gold_path, 'output': filename, 'check': diff_exists, 'load_lines': False, 'backup': True, 'gold_default': None, 'name': "output file %s exists" % (filename) }
    return make_check

checks = {
## optional checks, uncomment to enable these checks
    "devowel": { 'stdout': diff_almost_exact },
    "noduplicates": { 'stdout': diff_almost_exact },
    "freq": { 'stdout': diff_freqs },
## mandatory checks follow:
    "virahanka": { 'stdout': diff_almost_exact, 'stderr': diff_almost_exact },
    "segment": { 'stdout': print_fmeasure },
}

check.check_all(checks, extra_usage=__doc__.rstrip('\n\r'))

