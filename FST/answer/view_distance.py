#!/home/dif/Programs/anaconda/bin/python
def view_distance(target, source, insertcost, deletecost, replacecost):
    n = len(target)+1
    m = len(source)+1
    # set up dist and initialize values
    dist = [ [0 for j in range(m)] for i in range(n) ]
    for i in range(1,n):
        dist[i][0] = dist[i-1][0] + insertcost
    for j in range(1,m):
        dist[0][j] = dist[0][j-1] + deletecost
    
    # align source and target strings
    vtarget = []
    valign = []
    vsource = []
    for j in range(1,m):
        for i in range(1,n):
            inscost = insertcost + dist[i-1][j]
            delcost = deletecost + dist[i][j-1]
            if (source[j-1] == target[i-1]): add = 0
            else: add = replacecost
            substcost = add + dist[i-1][j-1]
            dist[i][j] = min(inscost, delcost, substcost)
    #track back
    i = n - 1
    j = m - 1
    while i + j > 0:
        inscost = insertcost + dist[i-1][j]
        delcost = deletecost + dist[i][j-1]
        if (source[j-1] == target[i-1]): add = 0
        else: add = replacecost
        substcost = add + dist[i-1][j-1]
           
        if dist[i][j] == inscost:
            vtarget.append(target[i-1])
            valign.append(" ")
            vsource.append("_")
            i = i - 1
        elif dist[i][j] == delcost:
            vtarget.append("_")
            valign.append(" ")
            vsource.append(source[j-1])
            j = j - 1
        else:
            vtarget.append(target[i-1])
            valign.append("|")
            vsource.append(source[j-1])
            i = i - 1
            j = j - 1
    vtarget.reverse() #notice here, list.reverse() does not return a value!
    valign.reverse()
    vsource.reverse()
    # return min edit distance
    return (dist[n-1][m-1], vtarget, valign, vsource)

if __name__=="__main__":
    from sys import argv
    if len(argv) > 2: 
        d, t, a, s = view_distance(argv[1], argv[2], 1, 1, 2)
        print "levenshtein distance =", d            
        print " ".join(t)
        print " ".join(a)
        print " ".join(s)
        