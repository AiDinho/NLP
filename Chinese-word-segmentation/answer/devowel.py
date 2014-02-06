import re
text = open('../testcases/default.in', 'r').read()
frac = re.findall(r'[^aeiou]',text)
print ''.join(frac)