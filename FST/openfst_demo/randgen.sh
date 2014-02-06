fstrandgen strings.fst | fstproject --project_output | fstprint --acceptor --isymbols=words.voc | awk '{printf("%s ", $3)} END{printf("\n")}'
