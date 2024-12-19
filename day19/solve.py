#
# Advent of Code 2024
# Bryan Clair
#
# Day 19
#
import sys
sys.path.append("..")
import aocutils
import functools

args = aocutils.parse_args()

intext = open(args.file).read()
ttext,ptext = intext.split('\n\n')
towels = [x.strip() for x in ttext.split(',')]

patterns = [x.strip() for x in ptext.strip().split('\n')]

towelre = "^(" + "|".join(towels) + ")*$"

import re
parser = re.compile(towelre)


part1, part2 = 0,0

@functools.cache
def matcher(s):
    if s == '':
        return 1
    count = 0
    for t in towels:
        if t == s[:len(t)]:
            count += matcher(s[len(t):])
    return count

for p in patterns:
    if parser.match(p):
        part1 += 1
    part2 += matcher(p)

print('part1:',part1)
print('part2:',part2)
