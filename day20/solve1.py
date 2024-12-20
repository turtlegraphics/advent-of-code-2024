#
# Advent of Code 2024
# Bryan Clair
#
# Day 20
#

print('Bullshit problem, this code solves a more interesting part 2.')

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

tracklen = 0
for p in track:
    if track[p] == 'S':
        startpos = p
        track[p] = '.'
    if track[p] == 'E':
        endpos = p
        track[p] = '.'
    if track[p] == '.':
        tracklen += 1

(sdist,sprev) = track.dijkstra(source = startpos, target = None,
                             distance_function = lambda u,v: 1 if track[u] == '.' and track[v] == '.' else None)
nocheat = sdist[endpos]
print('nocheat time:',nocheat)

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

def cheatdist(u,v):
    if track[u] == '#' and track[v] == '#':
        return 1
    if track[u] == '#' and track[v] == '.':
        return 1
    return None

hist = [0]*10000

def cheat(source):
    sx,sy = source
    source = (sx,sy)
        
    dist = {}
    prev = {}
    Q = set()
    Q.add(source)
    dist[source] = 0
    visited = set()

    while Q:
        # find min distance point u
        min_dist = float("inf")
        for p in Q:
            if dist[p] < min_dist:
                min_dist = dist[p]
                u = p

        Q.remove(u)
        visited.add(u)
        
        # update u's neighbors
        nbrs = track.neighbors(u)
        for v in nbrs:
            v = (v.x,v.y)
            if v in visited:
                continue
            dv = dist[u] + 1
            if dv == 20:
                continue

            if v in Q:
                if dv < dist[v]:
                    dist[v] = dv
            else:
                Q.add(v)
                dist[v] = dv
    return dist

for p in track:
    if track[p] == '.':
        tracklen -= 1
        print(tracklen)
        
        track[p] = '#'
        wdist = cheat(p)
        #print(p,wdist)
        
        for q in track:
            if track[q] == '.':
                try:
                    wd = wdist[q]
                except KeyError:
                    continue
                t = sdist[p] + wd + edist[q]
                if t < nocheat:
                    #print(sdist[p],p,wd,q,edist[q])
                    hist[nocheat-t] += 1
                    if nocheat - t >= 100:
                        part2 += 1
                    
        track[p] = '.'

for i in range(50,100):
    if hist[i] > 0:
        print(hist[i],'saving',i)
    
print('part1:',part1)
print('part2:',part2)
