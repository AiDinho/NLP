
from myfst import fst 

class myFST(fst.FST):
    def recognize(self, input, output):
        # insert your code here
        out = self.transduce(input.split())
        if (output == " ".join(out)): return True
        else: return False

# example that uses the nltk FST class
f = myFST('example')

# first add the states in the FST
for i in range(1,6):
    f.add_state(str(i)) # add states '1' .. '5'

# add one initial state
f.initial_state = '1'              # -> 1

# add all transitions
f.add_arc('1', '2', ('c'), ('1sdfs'))  # 1 -> 2 [a:1]
f.add_arc('2', '2', ('a'), ('0'))  # 2 -> 2 [a:0]
f.add_arc('2', '2', ('b'), ('1'))  # 2 -> 2 [b:1]
f.add_arc('2', '2', ('d'), ('1'))  # 2 -> 2 [b:1]
f.add_arc('2', '3', (), ('1'))     # 2 -> 3 [:1]
f.add_arc('3', '4', ('b'), ('1'))  # 3 -> 4 [b:1]
f.add_arc('4', '5', ('b'), ())     # 4 -> 5 [b:]

# add final state(s)
f.set_final('5')                   # 5 ->

# use the nltk transduce function
print " ".join(f.transduce("c b a b b".split()))

# use the recognize function defined in myFST


