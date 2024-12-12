#
# Advent of Code 2024
# Bryan Clair
#
# Day 12
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

done = aocutils.Grid(g)

def sameplant(u,v):
    if g[u] == g[v]:
        return 1
    else:
        return None

pf = aocutils.Grid(g)
w = pf.xmax
h = pf.ymax
for i in range(pf.width()):
    pf[(i,-1)] = '*'
    pf[(i,h+1)] = '*'
pf[(-1,-1)] = '*'
pf[(w+1,-1)] = '*'
for i in range(pf.height()-1):
    pf[(-1,i)] = '*'
    pf[(w+1,i)] = '*'

# print(pf)

for p in done:
    if done[p] == '.':
        continue
    plant = g[p]

#    print('working',p,'type',plant)
    (dist,prev) = g.dijkstra(p,target=None,
                             distance_function = sameplant)

    perim = 0

    for q in dist:
        done[q] = '.'
        for n in g.neighbors(q,validate=False):
            try:
                if g[n] != plant:
                    perim += 1
            except KeyError:
                perim += 1
    price1 = len(dist)*perim
    part1 += price1

    sides = 0
    for q in dist:
        (x,y) = q
        corner = 0
        for dx in [-1,1]:
            for dy in [-1,1]:
                px = (x+dx,y)
                py = (x,y+dy)
                pz = (x+dx,y+dy)
                if pf[pz] != plant and pf[px] == plant and pf[py] == plant:
                    corner += 1
                if pf[px] != plant and pf[py] != plant:
                    corner += 1
        sides += corner
    price2 = len(dist)*sides
    part2 += price2
    
print('part1:',part1)
print('part2:',part2)
