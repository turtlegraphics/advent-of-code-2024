#
# Advent of Code 2024
# Bryan Clair
#
# Day 02
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

def safe(v):
    d = (v[1] > v[0])
    for i in range(len(v)-1):
        if v[i+1] == v[i]:
            return False
        if ((v[i+1] > v[i]) != d):
            return False
        if abs(v[i+1]-v[i]) > 3:
            return False
    return True

for line in inputlines:
    v = [int(x) for x in line.split()]
    if safe(v):
        part1 += 1

    for i in range(len(v)):
        w = v[:i] + v[i+1:]
        if safe(w):
            part2 += 1
            break
    
print('part1:',part1)
print('part2:',part2)
