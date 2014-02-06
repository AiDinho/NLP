# creates the div by 4 FST we saw in the lecture notes
python create_input_fsa.py > input.fsa.txt
fstcompile --isymbols=binary.voc --osymbols=binary.voc binary.fst.txt > binary.fst
fstcompile --acceptor --isymbols=binary.voc input.fsa.txt > input.fsa
fstarcsort --sort_type=ilabel binary.fst | fstcompose input.fsa - | fstproject --project_output > result.fsa
fstprint --acceptor --isymbols=binary.voc result.fsa | awk '{print $3}' | grep -v '^$' | tr '\n' ' ' | sed
