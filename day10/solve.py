#
# Advent of Code 2024
# Bryan Clair
#
# Day 10
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

g = aocutils.Grid()
g.scan(inputlines)

heads = []
for loc in g:
    if g[loc] == '0':
        heads.append(loc)

reach = {}
ways = {}
for h in heads:
    r = []
    for x in range(10):
        r.append(set())
    r[0].add(h)
    reach[h] = r

    ways[h] = dict()
    ways[h][h] = 1
    
for h in heads:
    for t in range(9):
        for loc in reach[h][t]:
            count = ways[h][loc]
            for nbr in g.neighbors(loc):
                if g[nbr] == str(t+1):
                    reach[h][t+1].add(tuple(nbr))
                    try:
                        ways[h][tuple(nbr)] += count
                    except KeyError:
                        ways[h][tuple(nbr)] = count

for h in heads:
    part1 += len(reach[h][9])

for h in heads:
    for loc in reach[h][9]:
        part2 += ways[h][loc]
        
print('part1:',part1)
print('part2:',part2)
