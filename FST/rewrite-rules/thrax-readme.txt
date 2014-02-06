# This readme file explains how to use the rewrite rule to FST convertor that is part of the Thrax software package
# The Thrax web page is: http://www.openfst.org/twiki/bin/view/GRM/Thrax
# Thrax compiles context-dependent rewrite rules into FSTs that are compatible with the openfst toolkit

# To get you started on Thrax take a look at a simple Thrax grammar file: kiku.grm

# First step: create the Makefile that will run Thrax
# The -s option saves the symbols. Without this flag Thrax will replace symbols with integers for speed.
thraxmakedep -s kiku.grm 

# run make to create the FSTs
make

# The command 'thraxrewrite-tester' allows us to test the FSTs created from the rewrite rules
echo "input string: kikukukuku"

# left to right application
echo "left to right"
echo "kikukukuku" | thraxrewrite-tester --far=kiku.far --rules=KIKU_LTR

# right to left application
echo "right to left"
echo "kikukukuku" | thraxrewrite-tester --far=kiku.far --rules=KIKU_RTL

# simultaneous application
echo "simultaneous"
echo "kikukukuku" | thraxrewrite-tester --far=kiku.far --rules=KIKU_SIM
 
# using openfst to find the output of the rewrite rule for a given input
thraxmakedep -s kiku_input.grm 
make
# get individual FSTs from the far archive
farextract kiku.far
farextract kiku_input.far
# fstinfo KIKU_INPUT
fstcompose KIKU_INPUT KIKU_LTR > KIKU_OUTPUT
fstprint KIKU_OUTPUT | awk '{print $4}' | tr -d '\n' | awk '{print $1}'

