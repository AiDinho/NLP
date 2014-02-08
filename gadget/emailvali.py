import sys,re

def evali(rawAddr):
     return re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b', rawAddr)

if __name__ =="__main__":
    if(len(sys.argv)>1):
        lines = open(sys.argv[1], 'r').readlines()
        for line in lines:
            if line == '\n': continue
            if evali(line) == None: print "false"
            else: print "true"
            
        