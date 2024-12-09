#
# Advent of Code 2024
# Bryan Clair
#
# Day 09
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputline = open(args.file).read().strip()

# import re
# parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever
# name, val = parser.match(line).groups()
# val = int(val)

part1, part2 = 0,0

id = 0
pos = 0
c = 0
files = {}
freelist = []
while c < len(inputline):
    flen = int(inputline[c])
    files[id] = (pos,flen)
    try:
        gap = int(inputline[c+1])
        if (gap > 0):
            freelist.append((pos+flen,gap))
        pos += flen + gap
    except IndexError:
        pos += flen
    c += 2
    id += 1

# end of disk free space by force
freelist.append((pos,1))

maxid = id-1

disk = ['.']*pos
for id in range(maxid+1):
    (pos,flen) = files[id]
    for p in range(pos,pos+flen):
        disk[p] = id


nfree = len(freelist)-1

for id in range(maxid,0,-1):
    # move file
    #print()
    #print(''.join([str(x) for x in disk]))
    #print(freelist)
    (floc,flen) = files[id]
    #print('trying file',id,'length',flen)

    # make sure nfree is correct
    ploc,plen = freelist[nfree-1]
    while ploc > floc and nfree > 0:
        nfree -= 1
        ploc,plen = freelist[nfree-1]

    nloc,nlen = freelist[nfree]
    assert(nloc > floc)
    
    for ospot in range(len(freelist)):
        oloc, ogap = freelist[ospot]
        if oloc > floc:
            continue
        if flen > ogap:
            continue
        # print('gap of',ogap,'at',oloc)
        # move it on disk
        for p in range(floc,floc+flen):
            disk[p] = '.'
        for p in range(oloc,oloc+flen):
            disk[p] = id
        # update freelist

        # deal with the gap we put the file into
        if flen == ogap:
            # gap is gone
            freelist.pop(ospot)
            nfree -= 1
        else:
            # gap got smaller, moved right
            freelist[ospot] = (oloc+flen,ogap-flen)

        # add file's old location to freelist
        freelist.insert(nfree,(floc,flen))
        #print('insert')
        #print(freelist)

        # cleanup free list
        # nfree is index of newly created file free block
        
        npos,nlen = freelist[nfree+1]
        if floc + flen == npos:
            #print('combine with next')
            freelist[nfree] = (floc, flen + nlen)
            flen += nlen
            freelist.pop(nfree+1)

        if nfree == 0:
            break
        
        ppos,plen = freelist[nfree-1]
        if ppos + plen == floc:
            #print('combine with prev')
            freelist[nfree-1] = (ppos, plen + flen)
            freelist.pop(nfree)
            nfree -= 1
        break


for loc in range(len(disk)):
    if disk[loc] != '.':
        part2 += disk[loc]*loc

print('part2:',part2)
