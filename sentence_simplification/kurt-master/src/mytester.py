#!/usr/bin/env python3

from nltk import Tree

from loadrules import loadrules
from translate import translate

import debugutil, sys
debugutil.DEBUGGING = True#False #True

testerfi = open(sys.argv[1])
outputcheck = open(sys.argv[1][:sys.argv[1].index('_')]+'.output').readlines()

good = []
bad = []
def main():
	rules = loadrules('.'.join(sys.argv[1].split('.')[:-1])+'.yaml')
	trees = []
	for tr in testerfi.readlines():
		trees.append(Tree(tr))
	for i,tree in enumerate(trees):
		print('input: ', tree._pprint_flat('', ['(', ')'], False))
		transout = translate(tree, rules)
		try:
			if ' '.join(Tree(transout[1]).leaves()).lower() != ' '.join(Tree(outputcheck[i]).leaves()).lower():
				print('FAIL sent', i+1, ': ')
				print(transout[1])
				print(outputcheck[i])
				print(' '.join(Tree(transout[1]).leaves()).lower())
				print(' '.join(Tree(outputcheck[i]).leaves()).lower())
				bad.append(i+1)
				input('bad')
				#sys.exit(1)
			#translate(tree, rules)
			else:
				print('sent', i+1, ': ')
				print(transout[1])
				print(outputcheck[i])
				print(' '.join(Tree(transout[1]).leaves()).lower())
				print(' '.join(Tree(outputcheck[i]).leaves()).lower())
				good.append(i+1)
				#input('we got one')
		except TypeError:
			print ('skipping sent', i+1, '... no tree produced!')
			#print(transout[1])
			print(outputcheck[i])
			bad.append(i+1)
			input('bad -- no tree!')
	print('got these right: ')
	print(good)
	print('got these wrong: ')
	print(bad)
if __name__ == "__main__": main()
