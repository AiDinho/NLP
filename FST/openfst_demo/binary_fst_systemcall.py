import os
os.system("python create_input_fsa.py > input.fsa.txt")
os.system("fstcompile --isymbols=binary.voc --osymbols=binary.voc binary.fst.txt > binary.fst")
os.system("fstcompile --acceptor --isymbols=binary.voc input.fsa.txt > input.fsa")
os.system("fstarcsort --sort_type=ilabel binary.fst | fstcompose input.fsa - | fstproject --project_output > result.fsa")
os.system("fstprint --acceptor --isymbols=binary.voc result.fsa | awk '{print $3}' | grep -v '^$' | tr '\n' ' ' | sed")
