import codecs

prob = {}
N = float(0.0) 

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
        return prob[word]
    except:
        p = 100
        if len(word) < 3:
            p = 100000
        return 10./(N*p**len(word)) #the penalty is really really important
        
def splits(charlist):
    return [("".join(charlist[:i+1]), "".join(charlist[i+1:]))
            for i in range(len(charlist))]

def Pwords(words):
    product = 1
    for w in words:
        product = product * Pw(w)
    return product
    
def memo(f):
    "Memoize function f."
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
text = codecs.open("../zhwseg.in","r",encoding="utf-8").readlines()
for line in text:
    s = ""
    for w in segment(line.rstrip()):
        s = s+"||"+w
    print s
