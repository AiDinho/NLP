import sys
import codecs
import nltk

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
    #output.write("Score: %.2f" % ((score/len(a))*100))
    sys.stdout = old
    return True

if __name__ == '__main__':
    if len(sys.argv) > 2:
        with open(sys.argv[1], 'r') as a:
            with open(sys.argv[2], 'r') as b:
                print_fmeasure(list(a), list(b), sys.stdout)
    else:
        print >>sys.stderr, "usage: python", sys.argv[0], "output gold"

    
