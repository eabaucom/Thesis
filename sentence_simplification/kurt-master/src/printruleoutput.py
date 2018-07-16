#!/usr/bin/env python3

from nltk import Tree

from loadrules import loadrules
from translate import translate

import debugutil, sys
debugutil.DEBUGGING = False #True

rules = loadrules(sys.argv[1])
testerfi = open(sys.argv[2])

good = []
bad = []
def main():
	trees = []
	for tr in testerfi.readlines():
		trees.append(Tree(tr))
	for i,tree in enumerate(trees):
		#print('input: ', tree._pprint_flat('', ['(', ')'], False))
		transout = translate(tree, rules)
		
if __name__ == "__main__": main()
