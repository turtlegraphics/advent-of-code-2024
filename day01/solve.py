#
# Advent of Code 2024
# Bryan Clair
#
# Day 01
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

id1 = []
id2 = []

for line in inputlines:
    a,b = line.split()
    id1.append(int(a))
    id2.append(int(b))

id1.sort()
id2.sort()
part1 = 0
for i in range(len(id1)):
    d = abs(id1[i] - id2[i])
    part1 += d

print('part1:',part1)

part2 = 0
for l in id1:
    for m in id2:
        if l == m:
            part2 += l
print('part2:',part2)
