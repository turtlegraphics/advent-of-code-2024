#
# Advent of Code 2024
# Bryan Clair
#
# Day 07
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

def possible(val,nums,cat = False):
    """process right to left"""
    if val < 0 or val != int(val):
        return False
    
    n = nums.pop()
    if len(nums) == 0:
        nums.append(n)
        return val == n
    # try +
    if possible(val - n, nums,cat):
        nums.append(n)
        return True
    # try *
    if possible(val/n, nums,cat):
        nums.append(n)
        return True

    # try ||
    if cat:
        tenpow = int('1'+'0'*len(str(n)))
        if (val - n) % tenpow == 0 and possible((val - n)/tenpow, nums,cat):
            nums.append(n)
            return True
        
    nums.append(n)
    return False

for line in inputlines:
    test,numstr = line.split(':')
    nums = [int(n) for n in numstr.split()]
    test = int(test)
    if possible(test,nums):
        part1 += test
        part2 += test
    elif possible(test,nums,cat=True):
        part2 += test

        

print('part1:',part1)
print('part2:',part2)
