import fst

A = fst.Transducer()

A.add_arc(0, 1, 'a', 'q', 1.0) # the weights can be all set to 1 if you do not have probabilities as in HW2
A.add_arc(1, 1, 'c', 's', 1)
A.add_arc(0, 2, 'a', 'r', 2.5)
A[2].final = 2.5
A[1].final = 0

print A