import sys

cdecfi = open(sys.argv[1]).readlines()
alignfi = open(sys.argv[2]).readlines()

assert len(cdecfi) == len(alignfi)

for i in xrange(0, len(cdecfi)):
    cdecline = cdecfi[i].strip()
    alignline = alignfi[i].strip()

    sourcewords = cdecline.split(' ||| ')[0].split()
    targetwords = cdecline.split(' ||| ')[1].split()
    aligntups = [tuple(x.split('-')) for x in alignline.split()]

    mysourceline = ''
    mytargetline = ''

    sourceleftovers = sourcewords[:]
    targetleftovers = targetwords[:]

    for mytup in aligntups:
        mysourceline += sourcewords[int(mytup[0])]+'\t'
        mytargetline += targetwords[int(mytup[1])]+'\t'
        sourceleftovers[int(mytup[0])] = ''
        targetleftovers[int(mytup[1])] = ''
    mysourceline += '%% '+' '.join(sourceleftovers)
    mytargetline += '%% '+' '.join(targetleftovers)

    print mysourceline
    print mytargetline
