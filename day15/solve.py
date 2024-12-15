#
# Advent of Code 2024
# Bryan Clair
#
# Day 15
#
import sys
import time
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

(boardstr,movestr) = open(args.file).read().split('\n\n')

boardstr0 = [x.strip() for x in boardstr.split()]

doubled = {'#':'##','O':'[]','.':'..','@':'@.'}

boardstr = []
for line in boardstr0:
    row = ''
    for c in list(line):
        row += doubled[c]
    boardstr.append(row)

board = aocutils.Grid()
board.scan(boardstr)
moves = [x for x in list(movestr) if x != '\n']

for p in board:
    if board[p] == '@':
        robot = aocutils.Point(p)

dirs = {
    '<': aocutils.Point(-1,0),
    '>': aocutils.Point(1,0),
    '^': aocutils.Point(0,1),
    'v': aocutils.Point(0,-1),
}

def pushEW(b,d):
    """Push box whose left part is a point b in direction dir"""
    assert(board[b] == '[')
    if d == dirs['<']:
        check = b + d
        if board[check] == '#':
            return False
        if board[check] == ']':
            push(check + d,d)
            if board[check] == ']':
                return False
        assert(board[check] == '.')
        board[check] = '['
        board[b] = ']'
        board[b - d] = '.'
        return True

    if d == dirs['>']:
        check = b + d + d
        if board[check] == '#':
            return False
        if board[check] == '[':
            push(check,d)
            if board[check] == '[':
                return False
        assert(board[check] == '.')
        board[check] = ']'
        board[b + d] = '['
        board[b] = '.'
        return True

    return False

def canpushNS(b,d):
    checkL = b + d
    checkR = checkL + dirs['>']
    
    if board[checkL] == '#' or board[checkR] == '#':
        return False

    if board[checkL] == '[':
        return canpushNS(checkL,d)

    leftok = False
    rightok = False

    if board[checkL] == ']':
        if not canpushNS(checkL + dirs['<'],d):
            return False

    if board[checkR] == '.':
        return True

    assert(board[checkR] == '[')

    return canpushNS(checkR,d)

def pushNS(b,d):
    checkL = b + d
    checkR = checkL + dirs['>']

    if board[checkL] == '[':
        pushNS(checkL,d)
        
    if board[checkR] == '[':
        pushNS(checkR,d)

    if board[checkL] == ']':
        pushNS(checkL + dirs['<'],d)

    assert(board[checkL] == '.')
    assert(board[checkR] == '.')
    
    board[checkL] = '['
    board[checkR] = ']'
    board[b] = '.'
    board[b+dirs['>']] = '.'


def push(b,d):
    if d.y == 0:
        return pushEW(b,d)

    if canpushNS(b,d):
        pushNS(b,d)
        
for m in moves:
    if args.verbose:
        print(board)
        time.sleep(0.05)
        
#    if input() == 'q':
#        sys.exit()
    
    board[robot] = '.'
    d = dirs[m]
    pos = robot + d
    
    if board[pos] == '[':
        push(pos,d)
    elif board[pos] == ']':
        push(pos + dirs['<'],d)

    if board[pos] == '.':
        robot += d
        
    board[robot] = '@'
    
part2 = 0

for p in board:
    if board[p] == '[':
        (x,y) = p
        part2 += 100*(board.height() - y - 1) + x

print('part2:',part2)
print('for a fun animation, set your terminal to 100x51 and run with -v option')
