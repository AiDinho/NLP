import codecs, re

prob = {}
N = float(0.0) 
rex1 = re.compile(ur'^\d+[\u6708\u4E2A%]\Z',re.UNICODE)

def probGen():
    global prob, N    
    lines = codecs.open("../zh-wseg.train.utf8","r",encoding="utf-8").readlines()
    for line in lines:
        freq = float(line.split()[0])
        N = N + freq
    for line in lines:
        w = line.split()
        char = w[1]
        p = float(w[0])/N
        t = {char: p}
        prob.update(t)
    
def Pw(word):
    try:
        if rex1.match(word):
            print word
            return 0.01
        return prob[word]
    except:
        return 1000./(N*10000**len(word))
        
def splits(charlist, L=5):
    return [("".join(charlist[:s+1]), "".join(charlist[s+1:]))
            for s in range(min(len(charlist),L))]

def Pwords(words):
    product = 1
    for w in words:
        product = product * Pw(w)
    return product
    
def memo(f):
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo
    
@memo
def segment(sentence):
    if not sentence: return []
    charlist = list(sentence)
    candidates = [[first]+segment(rem) for first,rem in splits(charlist)]
    return max(candidates, key=Pwords)

probGen()
text = codecs.open("../zhwtest.in","r",encoding="utf-8").readlines()
for line in text:
    line = line[:-1]
    lines = line.split(" ")
    output = []
    for line in lines:
        output = output + segment(line)
    print " ".join(output)
