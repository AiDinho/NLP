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
    if n == 0: return [""]
    if n == 1: return ["S"]
    s = ["S" + prosody for prosody in virahanka(n-1)]
    l = ["L" + prosody for prosody in virahanka(n-2)]
    return s+l

if __name__ == "__main__":
    import sys
    for num in sys.stdin:
        n = int(num)
        print str(virahanka(n))
