#
# Advent of Code 2024
# Bryan Clair
#
# Day 16
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

maze = aocutils.Grid()
maze.scan(inputlines)

for p in maze:
    if maze[p] == 'S':
        start = p
        maze[p] = '.'
    if maze[p] == 'E':
        target = p
        maze[p] = '.'

def search(source):
    dist = {}
    prev = {}
    Q = set()
    Q.add(source)
    dist[source] = 0
    prev[source] = None
    visited = set()

    while Q:
        min_dist = 10000000000000
        for p in Q:
            if dist[p] < min_dist:
                min_dist = dist[p]
                u = p

        up,ud = u
        if up == target:
            return (dist, prev)

        Q.remove(u)
        visited.add(u)

        # make list of neighbors
        nbrs = []
        distuv = {}
        fwd = aocutils.Point(up)
        fwd += aocutils.Point(ud)
        if maze[fwd] == '.':
            v =  ((fwd.x,fwd.y),ud)
            nbrs.append(v)
            distuv[v] = 1

        v = (up,dirs[(dirs.index(ud)+1) % 4])
        nbrs.append(v)
        distuv[v] = 1000

        v = (up,dirs[(dirs.index(ud)-1) % 4])
        nbrs.append(v)
        distuv[v] = 1000
        
        # update u's neighbors
        for v in nbrs:
            if v in visited:
                continue
            dv = dist[u] + distuv[v]
            if v in Q:
                if dv < dist[v]:
                    dist[v] = dv
                    prev[v] = [u]
                elif dv == dist[v]:
                    prev[v].append(u)
            else:
                Q.add(v)
                dist[v] = dv
                prev[v] = [u]
          
    return(dist,prev)

dirs = [(1,0),(0,1),(-1,0),(0,-1)]
dist,prev = search((start,(1,0)))

finish = -1
for loc in dist:
    p,d = loc
    if p == target:
        assert(finish == -1)
        finish = loc
        part1 = dist[(p,d)]

def markall(loc):
    p,d = loc
    maze[p] = 'O'
    if prev[loc]:
        for x in prev[loc]:
            markall(x)

markall(finish)

for x in maze:
    if maze[x] == 'O':
        part2 += 1
        
print('part1:',part1)
print('part2:',part2)
