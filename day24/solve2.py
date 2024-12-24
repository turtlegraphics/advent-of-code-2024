#
# Advent of Code 2024
# Bryan Clair
#
# Day 24
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


temp = gates['z31']
gates['z31'] = gates['mfm']
gates['mfm'] = temp

temp = gates['z11']
gates['z11'] = gates['ngr']
gates['ngr'] = temp

temp = gates['z06']
gates['z06'] = gates['fkp']
gates['fkp'] = temp

temp = gates['bpt']
gates['bpt'] = gates['krj']
gates['krj'] = temp

swaps = ['z31','mfm','z11','ngr','z06','fkp','bpt','krj']
swaps.sort()
print(','.join(swaps))
sys.exit()

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
    xs = bin(x)[2:].zfill(inbits)
    ys = bin(y)[2:].zfill(inbits)
    for i in range(inbits):
        tag = str(inbits-i-1).zfill(2)
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

def backtrace(values,out,correct,depth=''):
    assert(values[out] != correct)
    if out[0] in ['x','y']:
        return
    
    op,x1,x2 = gates[out]
    print(depth+out,gates[out])
    print(depth+' ' + out + ' =',values[out],correct)
    print(depth+' ' + x1 + ' =',values[x1])
    print(depth+' ' + x2 + ' =',values[x2])
    if op == 'AND' and values[x1] == 0:
        backtrace(values,x1,1,depth+'.')
    if op == 'AND' and values[x2] == 0:
        backtrace(values,x2,1,depth+'.')
    if op == 'OR' and values[x1] == 1:
        backtrace(values,x1,0,depth+'.')
    elif op == 'OR' and values[x2] == 1:
        backtrace(values,x2,0,depth+'.')
    elif op == 'OR':
        backtrace(values,x1,1,depth+'.')
        backtrace(values,x2,1,depth+'.')
                  
def test(x,y):
    z = x + y
    #print(x,'+',y,'=',z)
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

    for out in evalorder:
        op,x1,x2 = gates[out]
        if op == 'AND':
            v = values[x1] & values[x2]
        if op == 'OR':
            v = values[x1] | values[x2]
        if op == 'XOR':
            v = values[x1] ^ values[x2]
        values[out] = v
#        if out[0] == 'z' and correct_result[out] != v:
#            backtrace(values,out,correct_result[out])
#            return out

    return correct_result,values

print('part1:',calc(x_init,y_init))

def checkval(zout):
    possible = set(gates.keys())
    for i in range(1000):
        x = randint(0,pow(2,inbits))
        y = randint(0,pow(2,inbits))
        correct,result = test(x,y)
        for v in result:
            if result[v] != correct[zout] and v in possible:
                possible.remove(v)
    print(possible)

def slowtest(x,y):
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
                    done = False
        
    return correct_result,values

for i in range(10000):
    x = randint(0,pow(2,pow(2,inbits)))
    y = randint(0,pow(2,pos(2,inbits)))
    correct,result = test(x,y)
    for z in correct:
        if correct[z] != result[z]:
            print('fail!')
sys.exit()
    
goodlist = []
for step,g1 in enumerate(gates.keys()):
    print(len(gates.keys()) - step,g1)
    for g2 in gates.keys():
        if g2 <= g1:
            continue
        
        temp = gates[g1]
        gates[g1] = gates[g2]
        gates[g2] = temp

        good = True
        tries = 0
        while good and tries < 100:
            x = randint(0,pow(2,39))
            y = randint(0,pow(2,39))
            correct,result = slowtest(x,y)
            for z in correct:
                try:
                    if correct[z] != result[z]:
                        good = False
                except KeyError:
                    good = False
            tries += 1

        if good:
            print('found!',g1,g2)
            goodlist.append((g1,g2))
        temp = gates[g1]
        gates[g1] = gates[g2]
        gates[g2] = temp

for g1,g2 in goodlist:
    print('found',g1,g2)

#badzs = list(badzs)
#badzs.sort()
#print(badzs)

#print(possible)
