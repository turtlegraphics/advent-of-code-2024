#
# Advent of Code 2024
# Bryan Clair
#
# Day 21
#
# Solution to Part 1 as I coded it up for speed.
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

dirs = {
    '^' : (0,1),
    'v' : (0,-1),
    '<' : (-1,0),
    '>' : (1,0)
}

numgrid = aocutils.Grid()
numgrid.scan(['789','456','123','X0A'])
numgrid.pop((0,0))
numlocs = {}
for g in numgrid:
    numlocs[numgrid[g]] = g
#print(numlocs)

padgrid = aocutils.Grid()
padgrid.scan(['X^A','<v>'])
padgrid.pop((0,1))
padlocs = {}
for g in padgrid:
    padlocs[padgrid[g]] = g
#print(padlocs)
        
initial = ((2,1), (2,1), (2,0))
target = ((2,1), (2,1), (1,0))

def neighbors(state):
    nlist = []
    (r1,r2,num) = state
    r1nbrs = padgrid.neighbors(r1)
    # just move r1
    for n in r1nbrs:
        n = (n.x,n.y)
        nlist.append((n,r2,num))

    # activate r1:
    if padgrid[r1] != 'A':
        # just move r2
        dx,dy = dirs[padgrid[r1]]
        r2x,r2y = r2
        newr2 = (r2x + dx, r2y + dy)
        if (newr2 in padgrid):
            nlist.append((r1,newr2,num))
    else:
        # activate r2
        if padgrid[r2] != 'A':
            # just move num
            dx,dy = dirs[padgrid[r2]]
            numx,numy = num
            newnum = (numx + dx, numy + dy)
            if (newnum in numgrid):
                nlist.append((r1,r2,newnum))
        else:
            # output value
            pass  # not actually doing this

    return nlist

def dijkstra(source, target):
    dist = {}
    prev = {}
    Q = set()
    Q.add(source)
    dist[source] = 0
    prev[source] = None
    visited = set()

    while Q:
        # find min distance point u
        min_dist = float("inf")
        for p in Q:
            if dist[p] < min_dist:
                min_dist = dist[p]
                u = p

        if u == target:
            return (dist, prev)

        Q.remove(u)
        visited.add(u)

        # update u's neighbors
        nbrs = neighbors(u)
        for v in nbrs:
            if v in visited:
                continue
            dv = dist[u] + 1
            if v in Q:
                if dv < dist[v]:
                    dist[v] = dv
                    prev[v] = u
            else:
                Q.add(v)
                dist[v] = dv
                prev[v] = u

    return (dist, prev)

def punch(s):
    total = 0
    cur = initial
    print('at',cur)
    for c in list(s):
        goal = ((2,1),(2,1),numlocs[c])
        dist,prev = dijkstra(cur,goal)
        step = dist[goal]
        print(step,'to output',c)
        total += step + 1
        cur = goal
    return total

part1, part2 = 0,0

for line in inputlines:
    lsp = punch(line)
    val = int(line[0:3])
    part1 += lsp*val
    print('complexity',lsp,'*',val,'=',val*lsp)

print('part1:',part1)
print('part2:',part2)
