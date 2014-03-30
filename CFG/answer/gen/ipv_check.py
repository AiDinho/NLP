print "...Checking..."

fvocab = open("./Vocab.gr", "r")
fallow = open("./allowed_words.txt","r")

wvocab = []
wallow = []

nallow = []
nappear = []

for line in fvocab:
    row = line.split()
    if row == []:
        continue
    if row[0] == "#" or row[0] == "\n":
        continue
    wvocab.append(row[-1])

for line in fallow:
    row = line.split()
    if row == []:
        continue
    if row[0] == "#" or row[0] == "\n":
        continue
    wallow.append(row[-1])

wvocab.sort()
wallow.sort()

wvocab = set(wvocab)
wallow = set(wallow)

flag = 0
for w1 in wvocab:
    flag = 0
    for w2 in wallow:
        if w1 == w2:
            flag = 1
    if flag == 0:
        nallow.append(w1)
        
for w1 in wallow:
    flag = 0
    for w2 in wvocab:
        if w1 == w2:
            flag = 1
    if flag == 0:
        nappear.append(w1)
        
print 'Not allowed:', nallow
print 'Not appear:', nappear

fvocab.close()
fallow.close()