#
# Advent of Code 2024
# Bryan Clair
#
# Day 24
#
# Written after solving, in an attempt to actually automate the solution.
# The actual solve was a mess of by-hand work and random crap, and the
# remains of that are stored in solve2.py
#
# This code only works probabilistically, but it seems to do pretty well.
#

import sys
sys.path.append("..")
import aocutils
from random import randint

args = aocutils.parse_args()

inittxt,gattxt = open(args.file).read().split('\n\n')

inbits = 0
values = {}
for line in inittxt.split('\n'):
    w,v = line.split(': ')
    values[w] = int(v)
    if w[0] == 'x':
        num = int(w[1:])
        if num > inbits:
            inbits = num
inbits += 1  # number of input bits

outbits = 0
gates = {}
for line in gattxt.strip().split('\n'):
    tokens = line.split(' ')
    assert(tokens[3] == '->')
    gates[tokens[4]] = (tokens[1],tokens[0],tokens[2])
    if tokens[4][0] == 'z':
        num = int(tokens[4][1:])
        if num > outbits:
            outbits = num
outbits += 1

def wires_to_int(values, name):
    result = []
    for (wire,val) in values.items():
        if wire[0] == name:
            result.append((wire,val))
    result.sort(reverse = True)
    return(int(''.join([str(val) for (wire,val) in result]),2))

x_init = wires_to_int(values,'x')
y_init = wires_to_int(values,'y')

def correctsum(x,y):
    """Return True if the machine computes x+y correctly"""
    global gates
    z = x + y
    xs = bin(x)[2:].zfill(inbits)
    ys = bin(y)[2:].zfill(inbits)
    zs = bin(z)[2:].zfill(outbits)

    values = {}
    for i in range(inbits):
        tag = str(inbits-i-1).zfill(2)
        values['x' + tag] = int(xs[i])
        values['y' + tag] = int(ys[i])

    correct_result = {}
    for i in range(outbits):
        tag = str(outbits-i-1).zfill(2)
        correct_result['z' + tag] = int(zs[i])

    done = False
    while not done:
        done = True
        for out in gates:
            if out not in values:
                op,x1,x2 = gates[out]
                if x1 in values and x2 in values:
                    if op == 'AND':
                        v = values[x1] & values[x2]
                    if op == 'OR':
                        v = values[x1] | values[x2]
                    if op == 'XOR':
                        v = values[x1] ^ values[x2]
                    values[out] = v
                    if out[0] == 'z' and v != correct_result[out]:
                        return False
                    done = False

    for v in correct_result:
        if v not in values:
            return False
        
    return True


def test(bits,tries=100):
    for i in range(tries):
        x = randint(0,pow(2,bits)-1)
        y = randint(0,pow(2,bits)-1)
        if not correctsum(x,y):
            return False
    return True
        
def findswap(bits):
    """
    Look for a swap that fixes answers up to bits bits.
    Leaves the gates swapped.
    """
    global gates
    goodlist = []
    for step,g1 in enumerate(gates.keys()):
        # print(len(gates.keys()) - step,g1)
        for g2 in gates.keys():
            if g2 <= g1:
                continue

            temp = gates[g1]
            gates[g1] = gates[g2]
            gates[g2] = temp

            if test(bits,500):
                print('swapping',g1,g2)
                return (g1,g2)
                
            temp = gates[g1]
            gates[g1] = gates[g2]
            gates[g2] = temp

swaps = []

bits = 0
while bits < inbits:
    print('bit',bits,end=' : ')
    if test(bits):
        print('ok')
    else:
        (g1,g2) = findswap(bits+1)
        swaps.append(g1)
        swaps.append(g2)
    
    bits += 1

swaps.sort()
print('part2:', ','.join(swaps))
