#
# Advent of Code 2024
# Bryan Clair
#
# Day 05
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = open(args.file).read()

# import re
# parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever
# name, val = parser.match(line).groups()
# val = int(val)

part1, part2 = 0,0

inord,inupd = inputlines.split('\n\n')

after = {}
for line in inord.split():
    a,b = line.split('|')
    if a in after:
        after[a].append(b)
    else:
        after[a] = [b]

def elfsort(v):
    for i in range(len(v)-1):
        for j in range(i,len(v)-1):
            # swap j and j+1 if needed
            a = v[j]
            b = v[j+1]
            if b in after and a in after[b]:
                v[j] = b
                v[j+1] = a
            
for line in inupd.split():
    vals = line.split(',')
    correct = True
    for vi,v in enumerate(vals):
        if v in after:
            for w in after[v]:
                try:
                    wi = vals.index(w)
                except ValueError:
                    continue
                if wi < vi:
                    correct = False
    if correct:
        mid = len(vals)//2
        part1 += int(vals[mid])
    else:
        for t in range(1000):  # fucken embarrassing
            elfsort(vals)
        mid = len(vals)//2
        print(vals[mid])
        part2 += int(vals[mid])
        

print('part1:',part1)
print('part2:',part2)
