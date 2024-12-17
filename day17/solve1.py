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


ip = 0
out = []

while True:
    try:
        inst = prog[ip]
        val = prog[ip+1]
    except IndexError:
        print(ip,'failed')
        break
    
    print(ip,':',opcodes[inst],val)
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
        out.append(str(get_combo(val) % 8))
    else:
        assert(False)

print('part1:',','.join(out))
