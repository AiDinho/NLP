prob = {}
N = float(0.0) 

def probGen():
    global prob, N    
    lines = open("../zh-wseg.train.utf8","r").readlines()
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
        return 10./(N*10**len(word))
        
probGen()

