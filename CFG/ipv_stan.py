import nltk

fbank = open("./stan2.bgr","r")
fs1 = open("./Stan.bgr","w")

print "...Generating..."

rule_set = []
productions = []


for line in fbank:
    tree = nltk.Tree(line)
    nltk.Tree.chomsky_normal_form(tree)
    productions = nltk.Tree.productions(tree)
    rule_set = rule_set + productions

n_rule_set = []
count = 0
for rule in rule_set:
    s_rule = str(rule)    
    s_rule = s_rule.replace("->"," ")
    row = s_rule.split()
    tag = row[0]
    if row[1][0] == "'" or row[1][0] == "\"":   # remove terminals
        new_row = tag + " "+ tag + "_t"
    else:
        new_row = s_rule
    n_rule_set.append(new_row)

fd = nltk.FreqDist(rule for rule in n_rule_set)
n_rule_set = list(set(n_rule_set))
n_rule_set.sort()    # to make S1.gr looks nice

for rule in n_rule_set:
     fs1.write(str(fd[rule])+" "+str(rule)+"\n")
     
print "...Finish!"

fbank.close()
fs1.close()
