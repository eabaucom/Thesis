from nltk.tree import Tree
import sys

filines = open(sys.argv[1]).readlines()

for line in filines:
    print ' '.join(Tree(line).leaves())
