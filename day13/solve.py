#
# Advent of Code 2024
# Bryan Clair
#
# Day 13
#
import sys
sys.path.append("..")
import aocutils
import re

args = aocutils.parse_args()

infile = open(args.file).read()
machs = infile.split('\n\n')
parser = re.compile(r"X.") #, Y\+(\d+)") # or whatever

machines = []
for m in machs:
    lines = m.strip().split('\n')
    pts = []
    for l in lines:
        c = '+' if l[0] == 'B' else '='
        bits = l.split(c)
        x = int(bits[1].split(',')[0])
        y = int(bits[2])
        pts.append(aocutils.Point(x,y))
    machines.append(pts)

def value(m):
    """Used for part 1 but the part 2 answer replaces it entirely."""
    print('machine')
    print(m[0],m[1],'prize:',m[2])
    best = None
    for a in range(100):
        for b in range(100):
            spot = m[0]*a + m[1]*b
            if spot == m[2]:
                print('found! a=',a,'b=',b)
                tokens = 3*a + b
                if best is None or tokens < best:
                    best = tokens
    if best:
        return best
    return 0

def bigvalue(m):
    A = m[0].x
    B = m[1].x
    C = m[0].y
    D = m[1].y
    P = m[2].x
    Q = m[2].y
    det = A*D - B*C
    if (det == 0):
        # Can't handle zero determinant case, luckily there aren't any
        print('Zero determinant!')
        print(m[0],m[1],'prize:',m[2])
        return None
        
    adet = D*P - B*Q
    bdet = -C*P + A*Q
    if (adet % det == 0) and (bdet % det == 0):
        return 3*adet//det + bdet//det
    return 0
    
part1, part2 = 0,0

for m in machines:
    part1 += bigvalue(m)

for m in machines:
    m[2] += aocutils.Point(10000000000000,10000000000000)
    part2 += bigvalue(m)

print('part1:',part1)
print('part2:',part2)
