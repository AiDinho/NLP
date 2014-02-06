
from fst import fst 
from collections import defaultdict

class myFST(fst.FST):

    def compose(self, f):
        new = myFST('composed %s and %s' % (self.label, f.label))
        return new

if __name__ == '__main__':

    # create FST1
    f1 = myFST('example1')
    # first add the states in the FST
    for i in range(0,4):
        f1.add_state(str(i)) # add states '0' .. '3'

    # add one initial state
    f1.initial_state = '0'              # -> 0

    # add all transitions
    f1.add_arc('0', '0', ('a'), ('a'))  # 0 -> 0 [a:a]
    f1.add_arc('0', '1', ('a'), ('b'))  # 0 -> 1 [a:b]
    f1.add_arc('0', '2', ('b'), ('b'))  # 0 -> 2 [b:b]
    f1.add_arc('1', '3', ('b'), ('a'))  # 1 -> 3 [b:a]
    f1.add_arc('2', '3', ('b'), ('b'))  # 2 -> 3 [b:b]

    # add final state(s)
    f1.set_final('3')                   # 3 ->

    # create FST2
    f2= myFST('example2')
    # first add the states in the FST
    for i in range(0,3):
        f2.add_state(str(i)) # add states '0' .. '2'

    # add one initial state
    f2.initial_state = '0'              # -> 0

    # add all transitions
    f2.add_arc('0', '1', ('b'), ('a'))  # 0 -> 1 [b:a]
    f2.add_arc('1', '1', ('a'), ('d'))  # 1 -> 1 [a:d]
    f2.add_arc('1', '2', ('b'), ('a'))  # 1 -> 2 [b:a]
    f2.add_arc('1', '2', ('a'), ('c'))  # 1 -> 2 [a:c]

    # add final state(s)
    f2.set_final('2')                   # 2 ->

    #f1.print_arc_pairs(f2)

    # compose FST1 and FST2
    f3 = f1.compose(f2)
    print f3.label
    print "Initial State:", f3.initial_state
    for arc in f3.arcs():
        print f3.src(arc), f3.dst(arc), f3.in_string(arc), f3.out_string(arc)
        if f3.is_final(f3.dst(arc)):
            print "Final State:", f3.dst(arc)

