#
# Advent of Code 2024
# Bryan Clair
#
# Day 06
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

room = aocutils.Grid()
room.scan(inputlines)

# find start
for (x,y) in room:
    if room[x,y] == '^':
        sx,sy = x,y
room[sx,sy] = '.'

def dopath(sx,sy):
    beenthere = set()
    # return None if looped
    px,py = sx,sy
    dx,dy = 0,1
    trace = aocutils.Grid(room)
    trace[px,py] = 'X'
    while True:
        nx = px + dx
        ny = py + dy
        try:
            if room[nx,ny] == '#':
                dx,dy = dy,-dx
                if (px,py,dx,dy) in beenthere:
                    return 'LOOP'
                else:
                    beenthere.add((px,py,dx,dy))
            else:
                px,py = nx,ny
            trace[px,py] = 'X'
        except KeyError:
            break
    return trace

trace = dopath(sx,sy)
for (x,y) in trace:
    if trace[x,y] == 'X':
        part1 += 1

for (ox,oy) in room:
    print (ox,oy)
    if room[(ox,oy)] != '.':
        continue
    room[ox,oy] = '#'
    good = dopath(sx,sy)
    if good == 'LOOP':
        part2 += 1
        print('got one!',part2)
    room[ox,oy] = '.'

print('part1:',part1)
print('part2:',part2)
