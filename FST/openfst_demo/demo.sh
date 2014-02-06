# a simple demo that generates sentences from a very simple grammar specified as a finite-state machine
fstcompile --acceptor --isymbols=pos.voc sent.fsa.txt > sent.fsa
#fstprint --acceptor --isymbols=pos.voc sent.fsa
fstdraw --isymbols=pos.voc sent.fsa | dot -Tps > sent.eps
epstopdf sent.eps
fstcompile --isymbols=pos.voc --osymbols=words.voc dict.fst.txt > dict.fst
fstcompose sent.fsa dict.fst > strings.fst
fstdraw --isymbols=pos.voc --osymbols=words.voc strings.fst | dot -Tps > strings.eps
epstopdf strings.eps
fstrandgen strings.fst | fstproject --project_output | fstprint --acceptor --isymbols=words.voc | awk '{printf("%s ", $3)} END{printf("\n")}'
