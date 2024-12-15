#
# Advent of Code 2024
# Bryan Clair
#
# Day 15
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

(boardstr,movestr) = open(args.file).read().split('\n\n')

boardstr = [x.strip() for x in boardstr.split()]

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

for m in moves:
    board[robot] = '.'
    pos = aocutils.Point(robot)
    pos += dirs[m]
    
    if board[pos] == '.':
        robot += dirs[m]
    else:
        while board[pos] == 'O':
            pos += dirs[m]
        if board[pos] == '.':
            board[pos] = 'O'
            robot += dirs[m]
        
    board[robot] = '@'

print(board)

part1, part2 = 0,0

for p in board:
    if board[p] == 'O':
        (x,y) = p
        part1 += 100*(board.height() - y - 1) + x
        
print('part1:',part1)
print('part2:',part2)
