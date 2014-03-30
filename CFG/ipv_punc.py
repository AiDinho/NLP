import nltk

fbank = open("./atis3.treebank","r")
fs1 = open("./Punc_S1.gr","w")

print "...Generating..."

rule_set = []
productions = []

for line in fbank:
    tree = nltk.Tree(line)
    nltk.Tree.chomsky_normal_form(tree)
    productions = nltk.Tree.productions(tree)
    rule_set = rule_set + productions

n_rule_set = []
tag_set = []
count = 0
for rule in rule_set:
    s_rule = str(rule)    
    s_rule = s_rule.replace("->"," ")
    row = s_rule.split()
    tag = row[0]
    tag_set.append(tag)

tag_set = list(set(tag_set))
tag_set.sort()    # to make S1.gr looks nice


for tag in tag_set:
    print tag

fbank.close()
fs1.close()



