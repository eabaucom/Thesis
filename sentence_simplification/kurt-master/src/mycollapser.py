import sys

prev = ''
for line in open(sys.argv[1]).readlines():
    line = line.strip()
    if line.startswith('( ( ('):
        #print 'TIER 1'
        print line
    elif prev == '':
        #print 'TIER 2'
        prev = '( '+line
        continue
    else:
        #print 'TIER 3'
        print prev+' '+line+' )'
        prev = ''
