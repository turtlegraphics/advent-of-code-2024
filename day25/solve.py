#
# Advent of Code 2024
# Bryan Clair
#
# Day 25
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

things = open(args.file).read().split('\n\n')

locks = []
keys = []

for thing in things:
    rows = thing.strip().split()
    count = [0,0,0,0,0]
    what = rows[0][0]
    for r in range(7):
        for c in range(5):
            if rows[r][c] == what:
                count[c] += 1
    if what == '#':
        locks.append(count)
    else:
        keys.append(count)

part1, part2 = 0,0

for lock in locks:
    for key in keys:
        fit = True
        for pin in range(5):
            if key[pin] < lock[pin]:
                fit = False
                break
        if fit:
            part1 += 1
                
print('locks\n',locks)
print('keys\n',keys)

print('part1:',part1)
print('part2:',part2)
