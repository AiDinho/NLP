
openfst is the toolkit for creating and manipulating FSTs.

Thrax is the toolkit for rewrite rules.

Both toolkits have been installed for use at the CSIL Linux machines.
To use openfst commands or Thrax commands do the following:

cd $HOME
scp -r fraser.sfu.ca:~anoop/cmpt413/sw .

And then add ~/sw/bin to your PATH:

export PATH=~/sw/bin:$PATH

------------

Note that you only need to use the openfst toolkit for the
Japanese transliteration question. For the korean numbers
problem it is probably overkill.

There are two demos:

1) strings.fst -- creates a set of strings based on a simple grammar

2) binary.fst -- divides binary strings by 4

The *.fsa.txt files are finite-state automata and *.fst.txt are the
finite state transducers in text format. They have to be converted
to the openfst compiled format .fst

The *.voc files are the vocabulary files mapping the tokens used
in the transducers or acceptors to unique IDs. These are used for
fstcompile, fstprint, etc.

In the .voc files the empty category is - by convention and has to
be assigned to index 0.

The .sh files are shell scripts that can be run on the command line
by typing in 'sh <filename>.sh'. They typically execute the command
line openfst tools such as fstcompile, fstcompose, etc.

In order to understand how to use the openfst tools, read each line
of the shell scripts and execute them individually to check what
each step accomplishes towards the final goal.

The .py files call the command line openfst tools in different ways.
The file binary_fst_systemcall.py shows how easy it is to adapt
binary_fst.sh into a python program. A better way to use Python for
calling openfst programs is in binary_fst.py

----------

An important fact about openfst. You need to sort any arcs in an
FST that you wish to compose with another FST.

# The FSTs must be sorted along the dimensions they will be joined.
# In fact, only one needs to be so sorted.
# This could have instead been done for "model.fst" when it was created. 
$ fstarcsort --sort_type=olabel input.fst input_sorted.fst
$ fstarcsort --sort_type=ilabel model.fst model_sorted.fst

# Creates the composed FST. 
$ fstcompose input_sorted.fst model_sorted.fst comp.fst

# Just keeps the output label 
$ fstproject --project_output comp.fst result.fst

# Do it all in a single command line. 
$ fstarcsort --sort_type=ilabel model.fst | fstcompose input.fst - | fstproject --project_output result.fst

----------

Part of the demo is adapted from the worked example in the lecture notes
by Mark Hasegawa-Johnson:

http://www.isle.illinois.edu/sst/courses/minicourses/2009/lecture6.pdf

