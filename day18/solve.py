#
# Advent of Code 2024
# Bryan Clair
#
# Day 18
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

size = 70
goal = (size,size)
start = (0,0)

def find_exit(bytes):
    g = aocutils.Grid()
    for x in range(size+1):
        for y in range(size+1):
            g[x,y] = '.'
    for line in inputlines[:bytes]:
        x,y = [int(v) for v in line.split(',')]
        g[x,y] = '#'

    dist, prev = g.dijkstra(start, goal,
                            distance_function = lambda u,v : 1 if g[u] == '.' and g[v] == '.' else None)

    return dist[goal]
    
print('part1:',find_exit(1024))

for check in range(2871,2873):
    # print(check)
    try:
        find_exit(check)
    except KeyError:
        print('part2:',inputlines[check-1])
        break
    
