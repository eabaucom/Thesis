import numpy as np
from nltk.tree import ParentedTree

#parameter for how similar words should be to be considered "equal" (normalized levenshtein distance)
DISTANCE_THRESHOLD = 0.30

def commonstart(source, target):
    count = 0
    for i in xrange(0, min(len(source), len(target))):
        if source[i] == target[i]:
            count += 1
        else:
            return count
    return count

#Normalized Levenshtein distance
def levenshtein(source, target):
    if len(source) < len(target):
        return levenshtein(target, source)
 
    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)
 
    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))
 
    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1
 
        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s))
 
        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)
 
        previous_row = current_row
    #normalize, and give proportional credit to how many chars the strings share at their starts
    return float(previous_row[-1]) / (len(source) + commonstart(source, target))

#modified so that it works on lists instead of string, and tests for normalized levenshtein distance
#within a threshold instead of strict equality
'''def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if levenshtein(s1[x - 1], s2[y - 1]) < DISTANCE_THRESHOLD: #if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]'''
'''def longest_common_substring(s1, s2):
    chunk_list = set()
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    current, x_current = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if levenshtein(s1[x - 1], s2[y - 1]) < DISTANCE_THRESHOLD: #if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > current:
                    current = m[x][y]
                    x_current = x
            else:
                m[x][y] = 0
                chunk_list.add(tuple(s1[x_current - current: x_current]))
    return chunk_list'''
	
'''def common_chunks(slist1, slist2):
    chunk_list = []
    temp_chunk = []
    subidx = 0
    for i in xrange(0, len(slist1)):
        word1 = slist1[i]
        foundone = False
        for j in xrange(subidx, len(slist2)):
            word2 = slist2[subidx]
            if levenshtein(word1, word2) < DISTANCE_THRESHOLD:
                temp_chunk.append((i, subidx))
                foundone = True
                subidx += 1
                break
        if (not foundone and temp_chunk) or (foundone and i == len(slist1) - 1):
            chunk_list.append(temp_chunk)
            temp_chunk = []
            subidx = 0
    return chunk_list'''
	
def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest, y_longest = 0, 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if (levenshtein(s1[x - 1], s2[y - 1]) < DISTANCE_THRESHOLD) and (s1[x - 1] != '') and (s2[y - 1] != ''): #if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
                    y_longest = y
            else:
                m[x][y] = 0
    return (s1[x_longest - longest: x_longest], (x_longest - longest, x_longest), (y_longest - longest, y_longest))
	
def get_substrings(s1, s2, full, mylist):
    if full[0] != ['']:
        s1 = '$%^'.join(s1).replace('$%^'.join(full[0]), '', 1).split('$%^')
        s2 = '$%^'.join(s2).replace('$%^'.join(full[0]), '', 1).split('$%^')
    s1 = s1[:full[1][0]]+['']*(full[1][1]-full[1][0]-1)+s1[full[1][0]:]
    s2 = s2[:full[2][0]]+['']*(full[2][1]-full[2][0]-1)+s2[full[2][0]:]
    full = longest_common_substring(s1, s2)
    mylist.append(full)
    if full[0]:
        return get_substrings(s1, s2, full, mylist)
    else:
        return mylist
    
def fix_indices(mylist):
    '''
    Iteratively add index ranges of previous LCS's to the
    later ones, so that the indicies will be correct for the
    full sentence.
	'''
    '''
    newlist = [mylist[0]]
    for i in xrange(1, len(mylist)):
        s1_start = mylist[i][1][0]
        s1_end = mylist[i][1][1]
        s2_start = mylist[i][2][0]
        s2_end = mylist[i][2][1]
        for j in xrange(i-1, -1, -1):
            if s1_start in xrange(mylist[j][1][0], mylist[j][1][1]):
                s1_start += newlist[j][1][1] - newlist[j][1][0] 
                s1_end += newlist[j][1][1] - newlist[j][1][0]
                
        for j in xrange(i-1, -1, -1):
            if s2_start in xrange(mylist[j][2][0], mylist[j][2][1]):
                s2_start += mylist[j][2][1] - mylist[j][2][0] 
                s2_end += mylist[j][2][1] - mylist[j][2][0]
        newlist.append((mylist[i][0], (s1_start, s1_end), (s2_start, s2_end)))
    return newlist
    '''
    #TO DO: try traversing the list backwards ... then adding range whenever there's an earlier index
    newlist = mylist
    for i in xrange(0, len(newlist)):
        s1_start = newlist[i][1][0]
        s1_end = newlist[i][1][1]
        s1_range = s1_end - s1_start
        s2_start = newlist[i][2][0]
        s2_end = newlist[i][2][1]
        s2_range = s2_end - s2_start
        for j in xrange(i+1, len(newlist)):
            new_s1 = newlist[j][1]
            new_s2 = newlist[j][2]
            if s1_start < new_s1[0]:
                new_s1 = (new_s1[0]+s1_range, new_s1[1]+s1_range)
            if s2_start < new_s2[0]:
                new_s2 = (new_s2[0]+s2_range, new_s2[1]+s2_range)
            newlist[j] = (newlist[j][0], new_s1, new_s2)
    return newlist
	
import sys

simpfi = open(sys.argv[2]).readlines()
compfi = open(sys.argv[1]).readlines()

#print Tree(simpfi[0]).leaves()
#for chunk in common_chunks(Tree(simpfi[0]).leaves(), Tree(compfi[0]).leaves()):
#    print chunk
#    print [Tree(simpfi[0]).leaves()[tup[0]] for tup in chunk]
#print longest_common_substring(Tree(simpfi[0]).leaves(), Tree(compfi[0]).leaves())
for i in xrange(0, len(simpfi)):
    simptree = ParentedTree(simpfi[i].lower())
    comptree = ParentedTree(compfi[i].lower())

    chunk_list = get_substrings(comptree.leaves(), simptree.leaves(), ([''], (0,0), (0,0)), [])
    #print chunk_list
    #print comptree
    alignlist = []
    for chunk in chunk_list:
        #print chunk
        comprange = chunk[1]
        simprange = chunk[2]
        simpidx = simprange[0]
        for j in xrange(comprange[0], comprange[1]):
            alignlist.append(str(simpidx)+'-'+str(j))
            simpidx += 1
        try:
            compposition = comptree.treeposition_spanning_leaves(comprange[0], comprange[1])
            #print comptree.root[compposition]
        except:
            pass
        try:
            simpposition = simptree.treeposition_spanning_leaves(simprange[0], simprange[1])
        except:
            pass
    print ' '.join(alignlist)			
    
