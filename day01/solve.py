#
# Advent of Code 2023
# Bryan Clair
#
# Day --
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

for line in inputlines:
    print(line)

print('part1:',part1)
print('part2:',part2)
