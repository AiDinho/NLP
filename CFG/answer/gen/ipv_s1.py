import nltk

fbank = open("./atis3.treebank","r")
fs1 = open("./S1_grail.gr","w")

print "...Generating..."

rule_set = []
productions = []

for line in fbank:
    tree = nltk.Tree(line)
    nltk.Tree.chomsky_normal_form(tree)
    productions = nltk.Tree.productions(tree)
    rule_set = rule_set + productions

fd = nltk.FreqDist(rule for rule in rule_set)
rule_set = set(rule_set)

for rule in rule_set:
     if str(rule).split()[-1][0] == "'":
         continue
     fs1.write(str(fd[rule])+" "+str(rule)+"\n")
     
print "...Finish!"

fbank.close()
fs1.close()