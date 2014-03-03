import nltk
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.corpus import brown

def default_tag(tagged_sents):
    tag_fd = FreqDist()
    for sent in tagged_sents:
        for word, postag in sent:
            tag_fd.inc(postag)
    return str(tag_fd.max())

def usage(args):
    if len(args) > 1:
        print >>sys.stderr, "unknown args", args[1:]
    print >>sys.stderr, "usage: %s -h -i trainsection -o testsection -m method" % (args[0])
    print >>sys.stderr, """
    -h help
    -i training section ,e.g. 'news' or 'editorial'
    -o test section ,e.g. 'news' or 'editorial'
    -m method, e.g. 'default', 'regexp', 'lookup', 'simple_backoff', 'unigram', 'bigram', 'trigram'

    Do not type in the single quotes at the command line.
    """
    sys.exit(2)

if __name__ == '__main__':
    import sys
    import getopt

    try:
        (trainsection, testsection, method) = ('news', 'editorial', 'default')
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:m:", ["help", "train=", "test=", "method="])
    except getopt.GetoptError:
        usage(sys.argv)
    for o, a in opts:
        if o in ('-h', '--help'): usage([sys.argv[0]])
        if o in ('-i', '--train'): trainsection = a
        if o in ('-o', '--test'): testsection = a
        if o in ('-m', '--method'): method = a

    train = brown.tagged_sents(categories=trainsection)
    test = brown.tagged_sents(categories=testsection)
    
    # default tagger   
    default_tag = default_tag(train)
    default_tagger = nltk.DefaultTagger(default_tag)
    
    # regexp tagger
    # patterns that used to tag; Notice the order may affect the performance
    patterns = [    
        (r'.*ing$', 'VBG'),
        (r'.*ed$','VBD'),
        (r'.*es$','VBZ'),
        (r'.*ness$', 'NN'),  
        (r'.*ly$', 'RB'),          
        (r'.*able$', 'JJ'),               
        (r'.*ould$','MD'),
        (r'(The|the|A|a|An|an)$', 'AT'),  
        (r'.*\'s$', 'NN$'),
        (r'.*s$','NNS'),
        (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
        (r'.*', 'NN')
        ]
    regexp_tagger = nltk.RegexpTagger(patterns)
    
    # lookup tagger
    fd = nltk.FreqDist(brown.words(categories='news'))
    cfd = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))
    most_freq_words = fd.keys()[:1000]
    likely_tags = dict((word,cfd[word].max()) for word in most_freq_words)
    lookup_tagger = nltk.UnigramTagger(model=likely_tags)    
    
    # unigram backoff tagger
    unigram_tagger = nltk.UnigramTagger(train, backoff = default_tagger)
    
    # bigram backoff tagger    
    
    if method == 'default':
        # use default tagger
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    elif method == 'regexp':
        # use regexp tagger
        print "%s:test:%lf" % (method, regexp_tagger.evaluate(test))
    elif method == 'lookup':
        # use lookup tagger
        print "%s:test:%lf" % (method, lookup_tagger.evaluate(test))
    elif method == 'simple_backoff':
        # use simple backoff tagger
        most_freq_words = fd.keys()[:1500]
        likely_tags = dict((word,cfd[word].max()) for word in most_freq_words)
        lookup_tagger = nltk.UnigramTagger(model=likely_tags) 
   
        backoff_reg_tagger = nltk.RegexpTagger(patterns, backoff = default_tagger)
        lookup_tagger = nltk.UnigramTagger(model=likely_tags, backoff = backoff_reg_tagger)
        print "%s:test:%lf" % (method, lookup_tagger.evaluate(test))
    elif method == 'unigram':
        # use unigram backoff tagger
        print "%s:test:%lf" % (method, unigram_tagger.evaluate(test))
    elif method == 'bigram':
        # use bigram backoff tagger

        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    elif method == 'trigram':
        # use trigram backoff tagger
        default_tag = default_tag(train)
        default_tagger = nltk.DefaultTagger(default_tag)
        print "%s:test:%lf" % (method, default_tagger.evaluate(test))
    else:
        print >>sys.stderr, "unknown method"
        sys.exit(2)

