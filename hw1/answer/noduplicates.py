f = open("../testcases/default.in","r")
text = f.readlines()
collection = []
for line in text:
    flag = 0
    for i in collection:
        if i==line: 
            flag=1 #there is a duplicate already
    if flag==0:
        collection.append(line)
print "".join(collection)
            

    