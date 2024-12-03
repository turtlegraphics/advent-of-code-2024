#
# Advent of Code 2024
# Bryan Clair
#
# Day 03
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

part1, part2 = 0,0

import re
parser = re.compile(r"mul\([1-9][0-9]?[0-9]?,[1-9][0-9]?[0-9]?\)")
#parser = re.compile(r"mul\([0-9]*,[0-9]*\)")


def val(s):
    v = 0 
    """Return sum of mul(,) instructions in s"""
    for m in parser.findall(s):
        n1,n2 = m[4:-1].split(',')
        v += int(n1)*int(n2)
    return v

doing = True

for line in inputlines:
    part1 += val(line)
    
    goods = line.split("do()")
    if not doing:
        # drop first segment
        goods = goods[1:]
        if not goods:
            # nothing to do
            continue
    for g in goods:
        front = g.split("don't()")
        part2 += val(front[0])
    last = goods[-1]
    if last.find("don't()") > -1:
        doing = False
    else:
        doing = True

print('part1:',part1)
print('part2:',part2)
