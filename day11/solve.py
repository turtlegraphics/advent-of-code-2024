#
# Advent of Code 2024
# Bryan Clair
#
# Day 11
#
import sys
sys.path.append("..")
import aocutils
import functools

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

# import re
# parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever
# name, val = parser.match(line).groups()
# val = int(val)

part1, part2 = 0,0

stones = [int(x) for x in inputlines[0].split()]
print('start:',stones)


@functools.cache
def blinklen(x,depth):
    if depth == 0:
        return 1
    if x == 0:
        return blinklen(1,depth-1)
    s = str(x)
    if len(s) % 2 == 0:
        a = blinklen(int(s[:len(s)//2]),depth-1)
        b = blinklen(int(s[len(s)//2:]),depth-1)
        return a + b
    return blinklen(x*2024, depth-1)

def blink(stones):
    newstones = []
    for x in stones:
        if x == 0:
            newstones.append(1)
            continue
        s = str(x)
        if len(s) % 2 == 0:
            newstones.append(int(s[:len(s)//2]))
            newstones.append(int(s[len(s)//2:]))
            continue
        newstones.append(x * 2024)
    return newstones

for x in stones:
    part1 += blinklen(x,25)

for x in stones:
    part2 += blinklen(x,75)

print('part1:',part1)
print('part2:',part2)
