#
# Advent of Code 2024
# Bryan Clair
#
# Day 17
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

reg = {}

inputfile = open(args.file).read()
inittxt,progtxt = inputfile.split('\n\n')
for line in inittxt.split('\n'):
    junk,regt,val = line.split()
    reg[regt[0]] = int(val)

print(reg)

junk,progtxt = progtxt.split()
prog = [int(x) for x in progtxt.split(',')]
print(prog)

opcodes = {
    0:'adv',
    1:'bxl',
    2:'bst',
    3:'jnz',
    4:'bxc',
    5:'out',
    6:'bdv',
    7:'cdv'
    }

def get_combo(val):
    assert(val != 7)
    if val < 4:
        return val
    if val == 4:
        return reg['A']
    if val == 5:
        return reg['B']
    if val == 6:
        return reg['C']

def quine(init, view = False):
    reg['A'] = init
    reg['B'] = 0
    reg['C'] = 0
    
    ip = 0
    nextout = 0
    while True:
        try:
            inst = prog[ip]
            val = prog[ip+1]
        except IndexError:
            # print(ip,'failed')
            break

        if view:
            print(ip,':',opcodes[inst],val,f"A{reg['A']:b} B{reg['B']:b} C{reg['C']:b}")
        ip += 2

        if opcodes[inst] == 'adv':
            num = reg['A']
            denom = pow(2,get_combo(val))
            reg['A'] = num // denom
        elif opcodes[inst] == 'bdv':
            num = reg['A']
            denom = pow(2,get_combo(val))
            reg['B'] = num // denom
        elif opcodes[inst] == 'cdv':
            num = reg['A']
            denom = pow(2,get_combo(val))
            reg['C'] = num // denom
        elif opcodes[inst] == 'bxl':
            reg['B'] = reg['B'] ^ val
        elif opcodes[inst] == 'bxc':
            reg['B'] = reg['B'] ^ reg['C'] 
        elif opcodes[inst] == 'bst':
            reg['B'] = get_combo(val) % 8
        elif opcodes[inst] == 'jnz':
            if reg['A'] != 0:
                ip = val
        elif opcodes[inst] == 'out':
            outval = get_combo(val) % 8
            if view:
                print(outval)
            if outval != prog[nextout]:
                return nextout
            nextout += 1
        else:
            assert(False)

    return nextout

def search(where):
    bestdepth = 0
    best = 0
    for i in where:
        depth = quine(i)
        if depth == len(prog):
            print("found!",i)
            break
        if depth > bestdepth:
            bestdepth = depth
            best = i
            print(best,bestdepth)

# search(range(57528265000,57528266000))

quine(3,view=True)
