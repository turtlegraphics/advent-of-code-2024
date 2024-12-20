#
# Advent of Code 2024
# Bryan Clair
#
# Day 20
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

track = aocutils.Grid()
track.scan(inputlines)

blanks = []
for p in track:
    if track[p] == 'S':
        startpos = p
        track[p] = '.'
    if track[p] == 'E':
        endpos = p
        track[p] = '.'
    if track[p] == '.':
        blanks.append(p)
        
(sdist,sprev) = track.dijkstra(source = startpos, target = None,
                             distance_function = lambda u,v: 1 if track[u] == '.' and track[v] == '.' else None)
nocheat = sdist[endpos]

(edist,eprev) = track.dijkstra(source = endpos, target = None,
                             distance_function = lambda u,v: 1 if track[u] == '.' and track[v] == '.' else None)
assert(nocheat == edist[startpos])

cheats = {}
for p in track:
    if track[p] == '#':
        emin = 1000000
        smin = 1000000
        for npt in track.neighbors(p):
            n = (npt.x,npt.y)
            if track[n] == '.':
                emin = min(edist[n],emin)
                smin = min(sdist[n],smin)
        t = smin + emin + 2
        if (nocheat - t) >= 100:
            part1 += 1

remaining = len(blanks)
for p in blanks:
    remaining -= 1
    if remaining % 100 == 0:
        print(remaining)
    px,py = p
    dp = sdist[p]
    
    for q in blanks:
        qx,qy = q
        wd = abs(qx-px) + abs(qy-py)
        if wd > 20:
            continue
        t = dp + wd + edist[q]
        if nocheat - t >= 100:
            part2 += 1
    
print('part1:',part1)
print('part2:',part2)
