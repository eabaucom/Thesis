import sys
from nltk.tree import Tree

for line in open(sys.argv[1]).readlines():
    sys.stdout.write(' '.join(Tree(line.strip()).leaves())+'\n')
