#
# Advent of Code 2024
# Bryan Clair
#
# Day 24
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()


part1, part2 = 0,0

inittxt,gattxt = open(args.file).read().split('\n\n')

N = 0
values = {}
for line in inittxt.split('\n'):
    w,v = line.split(': ')
    values[w] = int(v)
    if w[0] == 'x':
        num = int(w[1:])
        if num > N:
            N = num
N += 1  # number of input bits

gates = {}
for line in gattxt.strip().split('\n'):
    tokens = line.split(' ')
    assert(tokens[3] == '->')
    gates[tokens[4]] = (tokens[1],tokens[0],tokens[2])


def wires_to_int(values, name):
    result = []
    for (wire,val) in values.items():
        if wire[0] == name:
            result.append((wire,val))
    result.sort(reverse = True)
    return(int(''.join([str(val) for (wire,val) in result]),2))

x_init = wires_to_int(values,'x')
y_init = wires_to_int(values,'y')

# solve part 1, keep track of the order of gate evaluation
evalorder = []
done = False
while not done:
    done = True
    for out in gates:
        if out not in values:
            op,x1,x2 = gates[out]
            if x1 in values and x2 in values:
                evalorder.append(out)
                if op == 'AND':
                    v = values[x1] & values[x2]
                if op == 'OR':
                    v = values[x1] | values[x2]
                if op == 'XOR':
                    v = values[x1] ^ values[x2]
                values[out] = v
                done = False

def calc(x,y):
    values = {}
    xs = bin(x)[2:].zfill(N)
    ys = bin(y)[2:].zfill(N)
    for i in range(N):
        tag = str(N-i-1).zfill(2)
        values['x' + tag] = int(xs[i])
        values['y' + tag] = int(ys[i])
    
    for out in evalorder:
        op,x1,x2 = gates[out]
        if op == 'AND':
            v = values[x1] & values[x2]
        if op == 'OR':
            v = values[x1] | values[x2]
        if op == 'XOR':
            v = values[x1] ^ values[x2]
        values[out] = v

    return wires_to_int(values,'z')

print('part1:',calc(x_init,y_init))
print('part2:',part2)
