import sys
from nltk.tree import Tree

fi = open(sys.argv[1]).readlines()

for line in fi:
    line = line.strip()
    if line == '': continue
    print ' '.join(Tree(line).leaves())

