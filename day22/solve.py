#
# Advent of Code 2024
# Bryan Clair
#
# Day 22
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

# import re
# parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever
# name, val = parser.match(line).groups()
# val = int(val)

part1, part2 = 0,0

prune = 0x1000000
assert(prune == 16777216)

def nextrand(x):
    x = ((x << 6)^x) & (prune-1)
    x = ((x >> 5)^x) & (prune-1)
    x = ((x << 11)^x) & (prune-1)
    return x

allfours = {}

t = len(inputlines)
for line in inputlines:
    if (t % 100) == 0:
        print(t)
    t -= 1
    
    fours = {}
    x0 = int(line)
    
    x1 = nextrand(x0)
    d0 = (x1 % 10) - (x0 % 10)
    
    x2 = nextrand(x1)
    d1 = (x2 % 10) - (x1 % 10)
    
    x3 = nextrand(x2)
    d2 = (x3 % 10) - (x2 % 10)
    
    for i in range(1997):
        x4 = nextrand(x3)
        d3 = (x4 % 10) - (x3 % 10)
        dseq = (d0,d1,d2,d3)
        if dseq not in fours:
            fours[dseq] = x4 % 10
        x3 = x4
        d0,d1,d2 = d1,d2,d3

    part1 += x4
    for dseq in fours:
        if dseq in allfours:
            allfours[dseq] += fours[dseq]
        else:
            allfours[dseq] = fours[dseq]

print()

print('part1:',part1)

for dseq in allfours:
    if allfours[dseq] > part2:
        part2 = allfours[dseq]
        bestseq = dseq

print('part2:',part2)
