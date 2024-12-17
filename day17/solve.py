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

inputfile = open(args.file).read()
inittxt,progtxt = inputfile.split('\n\n')

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

reg = {'A':0,'B':0,'C':0}

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


def run(init):
    reg['A'] = init
    reg['B'] = 0
    reg['C'] = 0
    
    ip = 0
    out = []

    while True:
        try:
            inst = prog[ip]
            val = prog[ip+1]
        except IndexError:
            #print(ip,'failed')
            break

        # print(ip,':',opcodes[inst],val)
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
            out.append(get_combo(val) % 8)
        else:
            assert(False)
    return out

def do_the_rest(tail,val):
    print('-'*tail,val)
    if tail < 0:
        print('part2:',val)
        return True
    
    target = prog[tail:]
    for a in range(8):
        v = run(val*8 + a)
        if v == target and do_the_rest(tail-1,val*8 + a):
            return True
        
    return False

do_the_rest(len(prog) - 1,0)
