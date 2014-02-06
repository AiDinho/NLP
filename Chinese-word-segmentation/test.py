lines = open("zh-wseg.train.utf8","r").readlines()
freq = {}
for line in lines:
    w = line.split()
    char = w[1]
    frequency = w[0]
    t={}
    t[char] = frequency 
    freq.update(t)
print freq    