#since we have up to 4-grams in the training data, we may use 4-grams model
import sys, codecs

    



def Pw(word):
    return freq[word]

def segment(text):
    table = [[""]]
    text = unisplit(text, 3)
    print text
    
    for i in range(500):
        print text[i]
    i = 0
    '''while (i <= len(text)):
        seg = splits([text[i],text[i+1],text[i+2],text[i+3]])
        i = i+1
'''
    
def splits(chunk):
    return
    
def unisplit(str, num):
    return [str[start:start+num] for start in range(0, len(str), num)]
    
def Pwords(words):
    product = 1    
    for w in words:
        product = product * Pw(w)
    return product

text = open("../zhwseg.in","r").read()
segment(text)


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
    
