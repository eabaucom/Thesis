import sys

fi = open(sys.argv[1]).readlines()

for line in fi:
    if not line.startswith('\t') or line.strip() == '': continue
    print line[line.index('('):].strip()
