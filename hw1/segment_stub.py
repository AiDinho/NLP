
import sys, codecs

if __name__ == '__main__':
    if len(sys.argv) > 1:
        old = sys.stdout
        sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
        # ignoring the dictionary provided in sys.argv[1]
        for line in sys.stdin:
            line = line[:-1]
            utf8line = unicode(line, 'utf-8')
            output = [i for i in utf8line]
            print " ".join(output)
        sys.stdout = old
    else:
        print >>sys.stderr, "usage: python", sys.argv[0], "frequencies < inputfile"
    
