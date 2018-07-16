import sys

fi = open(sys.argv[1]).readlines()

stack = []
for j in xrange(0, len(fi)):
    mywriter = open(sys.argv[1][:sys.argv[1].index('.')]+'.xml_'+str(j), 'w')
    for i,c in enumerate(fi[j]):
        if c == '(':
            mylabel = fi[j][i+1:fi[j].index(' ',i+1)]
            if mylabel == ',':
                mylabel = 'comma'
            elif mylabel == '.':
                mylabel = 'punctuation'
            elif mylabel == '':
                mylabel = 'top'
            stack.append(mylabel)
            mywriter.write((len(stack)-1)*'  '+'<'+mylabel+'>\n')
        elif c == ')':
            if fi[j][i-1] not in [' ','(',')']:
                myword = fi[j][fi[j].rindex(' ',0,i)+1:i]
                if myword == '"':
                    myword = '\\"'
                mywriter.write((len(stack))*'  '+'<word> '+myword+' </word>\n')
            mywriter.write((len(stack)-1)*'  '+'</'+stack.pop()+'>\n')
    mywriter.close()
