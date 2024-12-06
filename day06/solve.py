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
    """
    trace a path from starting position sx,sy
    return the traced path if it exits the room
    return 'LOOP' if it enters into a loop
    """
    
    # keep track of location/directions that are visited
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
                # turn right
                dx,dy = dy,-dx
                
                # check for loop
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
print('part1:',part1)

print('----- part 2 -----')

lastpct = 0
for (ox,oy) in room:
    if trace[(ox,oy)] != 'X':
        # no point blocking a path that's never used!
        continue

    # try dropping an obstacle here
    room[ox,oy] = '#'
    good = dopath(sx,sy)
    if good == 'LOOP':
        part2 += 1
    room[ox,oy] = '.'

    # report on progress
    pct_done = round(100*(1 - oy/room.height()))
    if (pct_done != lastpct) and (pct_done % 5 == 0):
        lastpct = pct_done
        print(pct_done, "% done", part2, "loops found so far")

    
print('------------------')
print('part2:',part2)
