from myfst import fst

class myFST(fst.FST):
    def recognize(self, input, output):
        # insert your code here
        return False

# you can define an FST either this way:
f = myFST.parse("example", """
    -> 1
    1 -> 2 [a:1]
    2 -> 2 [a:0]
    2 -> 2 [b:1]
    2 -> 3 [:1]
    3 -> 4 [b:1]
    4 -> 5 [b:]
    5 ->
    """)

# but if you wish to use methods defined in myFST
# then you must do it in this more verbose way
f = myFST('example')

# first add the states in the FST
for i in range(1,4):
    f.add_state(str(i)) # add states '1' .. '5'

# add one initial state
f.initial_state = '1'              # -> 1

# add all transitions
f.add_arc('1', '2', ('['), (''))
f.add_arc('2', '2', ('1'), (''))
f.add_arc('2', '2', ('0'), (''))
f.add_arc('2', '3', ('^'), (''))
f.add_arc('3', '3', ('2'), ('baek'))
f.add_arc('3', '3', ('3'), ('cheon'))
f.add_arc('3', '3', ('4'), ('man'))
f.add_arc('3', '3', ('8'), ('eok'))
f.add_arc('3', '1', (']'), (''))
f.add_arc('2', '1', (']'), ('sib'))    # 4 -> 5 [b:]

# add final state(s)
f.set_final('1')                   # 5 ->

# use the nltk transduce function
print " ".join(f.transduce("[ 1 0 ^ 8 ]".split()))

# use the recognize function defined in myFST


