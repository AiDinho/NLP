import codecs, sys

def read_katakana(kpron_stream):
    for line in kpron_stream:
        f = line.split()
        try:
            utf8char = unicode(f[0], 'utf-8')
            print utf8char, f[1]
        except:
            print >>sys.stderr, "Unexpected error: ", sys.exc_info()[0]
            raise

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "usage: %s filename" % (sys.argv[0])
        sys.exit(2)
    else:
        read_katakana(open(sys.argv[1]))
