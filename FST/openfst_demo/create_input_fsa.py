import sys
for line in sys.stdin:
    input = line.split()
    for (i,inp) in enumerate(input):
        print i, i+1, inp
    print len(input)
