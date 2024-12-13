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

machines = []
for m in infile.split('\n\n'):
    vals = [int(x) for x in re.findall(r'\d+', m)]
    machines.append(vals)
    
def tokens(m):
    A = m[0]
    C = m[1]

    B = m[2]
    D = m[3]

    P = m[4]
    Q = m[5]
    
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
    part1 += tokens(m)

for m in machines:
    m[4] += 10000000000000
    m[5] += 10000000000000
    part2 += tokens(m)

print('part1:',part1)
print('part2:',part2)
