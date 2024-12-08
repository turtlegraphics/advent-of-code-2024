#
# Advent of Code 2024
# Bryan Clair
#
# Day 08
#
import sys
sys.path.append("..")
import aocutils
import itertools
import math

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

g = aocutils.Grid()
g.scan(inputlines)

antennas = {}
for p in g:
    freq = g[p]
    if freq != '.':
        try:
            antennas[freq].append(p)
        except KeyError:
            antennas[freq] = [p]

anmap = aocutils.Grid(g)
for p in anmap:
    anmap[p] = '.'
    
antinodes1 = set()
antinodes2 = set()
for freq in antennas:
    for (p,q) in itertools.combinations(antennas[freq], 2):
        pp = aocutils.Point(p)
        qq = aocutils.Point(q)
        delta = pp - qq
        a1 = qq + delta + delta
        a2 = qq - delta
        if a1 in g:
            antinodes1.add(tuple(a1))
        if a2 in g:
            antinodes1.add(tuple(a2))

        # part 2
        delta //= math.gcd(delta.x,delta.y)
        while pp in g:
            antinodes2.add(tuple(pp))
            anmap[pp] = '#'
            pp -= delta
        while qq in g:
            antinodes2.add(tuple(qq))
            anmap[qq] = '#'
            qq += delta

print('part1:',len(antinodes1))
print('part2:',len(antinodes2))
