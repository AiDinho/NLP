import sys
import traceback

def norecurse(f):
     def func(*args, **kwargs):
         if len([l[2] for l in traceback.extract_stack() if l[2] == f.func_name]) > 0:
             raise Exception, 'recursion detected'
         return f(*args, **kwargs)
     print >>sys.stderr, "no recursion detected"
     return func

@norecurse
def virahanka(n):
    # change this function to be non-recursive by using a table to store computed results for each n
    table = [[""],["S"]]
    for i in range(n-1):
        vira1=vira2=[]        
        for piece in table[i+1]:
            vira1 = vira1 + ["S"+ piece]
        for piece in table[i]:
            vira2 = vira2 + ["L"+ piece]
        table.append(vira1+vira2)
    return table[n]

if __name__ == "__main__":
    import sys
    for num in sys.stdin:
        n = int(num)
        print str(virahanka(n))
