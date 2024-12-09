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
while c < len(inputline):
    flen = int(inputline[c])
    files[id] = (pos,flen)
    try:
        pos += flen + int(inputline[c+1])
    except IndexError:
        pos += flen
    c += 2
    id += 1
maxid = id-1

disk = [None]*pos
for id in range(maxid+1):
    (pos,flen) = files[id]
    for p in range(pos,pos+flen):
        disk[p] = id


loc = 0
for id in range(maxid,0,-1):
    # move file
    (pos,flen) = files[id]
    if loc >= pos:
        continue
    for p in range(pos,pos+flen):
        disk[p] = None
    while flen > 0:
        while disk[loc] is not None:
            loc += 1
        disk[loc] = id
        flen -= 1

for loc in range(len(disk)):
    if disk[loc] is None:
        break
    part1 += disk[loc]*loc

print('part1:',part1)
print('part2:',part2)
