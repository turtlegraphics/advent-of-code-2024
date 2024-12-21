#
# Advent of Code 2024
# Bryan Clair
#
# Day 21
#
import sys
sys.path.append("..")
import aocutils
import functools

args = aocutils.parse_args()
inputlines = [x.strip() for x in open(args.file).readlines()]

#
# Relatively easy way to create dictionaries that convert
# from a key character to a keypad location
#
numgrid = aocutils.Grid()
numgrid.scan(['789','456','123','X0A'])
numgrid.pop((0,0))
numlocs = {}
for g in numgrid:
    numlocs[numgrid[g]] = g

padgrid = aocutils.Grid()
padgrid.scan(['X^A','<v>'])
padgrid.pop((0,1))
padlocs = {}
for g in padgrid:
    padlocs[padgrid[g]] = g


@functools.cache
def paths(source,target):
    """
    Compute all motion paths to move robot from source key to target key.
    Returns a set containing one or two A-ending paths.
    """
    try:
        sx,sy = padlocs[source]
        tx,ty = padlocs[target]
    except KeyError:
        sx,sy = numlocs[source]
        tx,ty = numlocs[target]
        
    hpart = ''
    while tx > sx:
        hpart += '>'
        sx += 1
    while tx < sx:
        hpart += '<'
        sx -= 1

    vpart = ''
    while ty > sy:
        vpart += '^'
        sy += 1
    while ty < sy:
        vpart += 'v'
        sy -= 1

    if target in ['<','7','4','1'] and source in ['^','0','A']:
        # got to go vertical first
        return set([vpart + hpart + 'A'])

    if source in ['<','7','4','1'] and target in ['^','0','A']:
        # got to go horizontal first
        return set([hpart + vpart + 'A'])
    
    return set([vpart + hpart + 'A', hpart + vpart + 'A'])

@functools.cache
def complexity(outstr,robots):
    assert(outstr[-1] == 'A')
    
    if robots == 0:
        return len(outstr)

    tot = 0
    loc = 'A'
    for c in outstr:
        best = None
        for p in paths(loc,c):
            val = complexity(p,robots-1)
            if best is None or val < best:
                best = val
        tot += best
        loc = c

    assert(loc == 'A')

    return tot

part1, part2 = 0,0
for line in inputlines:
    c1 = complexity(line,2+1)
    c2 = complexity(line,25+1)
    val = int(line[0:3])
    part1 += c1*val
    part2 += c2*val
    
print('part 1:',part1)
print('part 2:',part2)
