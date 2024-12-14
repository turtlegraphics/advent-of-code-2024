#
# Advent of Code 2024
# Bryan Clair
#
# Day 14
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

import re

botp = []
botv = []

for line in inputlines:
    vals = [int(x) for x in re.findall(r'[\d-]+', line)]
    pos = aocutils.Point(vals[0],vals[1])
    vel = aocutils.Point(vals[2],vals[3])
    botp.append(pos)
    botv.append(vel)
    
roomsize = aocutils.Point(101,103)
# roomsize = aocutils.Point(11,7)



for t in range(20000):
    quads = dict()
    quads[(True,True)] = 0
    quads[(False,True)] = 0
    quads[(False,False)] = 0
    quads[(True,False)] = 0
    
    for i in range(len(botp)):
        pos = botp[i]
        pos += botv[i]
        pos.x %= roomsize.x
        pos.y %= roomsize.y
        botp[i] = pos
        
        if pos.x == roomsize.x // 2 or pos.y == roomsize.y // 2:
            continue
        quads[(pos.x < roomsize.x // 2,pos.y < roomsize.y // 2)] += 1

    qval = 1
    for q in quads:
        qval *= quads[q]

    if qval < 130000000:
        print(qval,t)
        g = aocutils.Grid()
        for p in botp:
            g[p] = '*'
        g.display(blank='.',vflip=True)
        x = input('Do you see the tree? (type y for yes):')
        if x == 'y':
            part2 = t + 1
            break
        
    if t == 99:
        part1 = qval
        
print('part1:',part1)
print('part2:',part2)
