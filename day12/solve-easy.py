#
# Advent of Code 2024
# Bryan Clair
#
# Day 12
#
# Re-written using (new) utility functions added to aocutils
#
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

part1, part2 = 0,0

g = aocutils.Grid()
g.scan(inputlines)

done = aocutils.Grid(g)

for p in done:
    if done[p] == '.':
        continue

    region = g.region(p)
    
    for q in region:
        done[q] = '.'
        
    area = len(region)
    
    part1 += area * g.perimeter(region)

    part2 += area * g.sides(region)

print('part1:',part1)
print('part2:',part2)
