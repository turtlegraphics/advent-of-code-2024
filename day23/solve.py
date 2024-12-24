#
# Advent of Code 2024
# Bryan Clair
#
# Day 23
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

# import re
# parser = re.compile(r"name:\s*(\w+)\s*val:\s*(\d+)") # or whatever
# name, val = parser.match(line).groups()
# val = int(val)

part1, part2 = 0,0

import scipy.sparse as ss
import numpy as np

index = {}
names = []
i = 0
for line in inputlines:
    sx,sy = line.split('-')
    if sx not in index:
        index[sx] = i
        names.append(sx)
        i += 1
    if sy not in index:
        index[sy] = i
        names.append(sy)
        i += 1

N = i
assert(len(names) == N)

A = ss.lil_array((N,N)) # all edges
TV = ss.lil_array((N,N)) # only edges connecting with T vertices
TTT = ss.lil_array((N,N)) # only T vertice and edges between them

for line in inputlines:
    sx,sy = line.split('-')
    x = index[sx]
    y = index[sy]
    A[x,y] = 1
    A[y,x] = 1

    if sx[0] == 't' or sy[0] == 't':
        TV[x,y] = 1
        TV[y,x] = 1

    if sx[0] == 't' and sy[0] == 't':
        TTT[x,y] = 1
        TTT[y,x] = 1

# going to count the number of times a tx appears in a triangle,
# the number of times it appears in a triangle with another ty,
# and the number of times it appears in a fully t triangle
A3 = A.dot(A).dot(A)
TV3 = TV.dot(TV).dot(TV)
TTT3 = TTT.dot(TTT).dot(TTT)

tri1s, tri2s, tri3s = 0,0,0

for s,t in index.items():
    if s[0] == 't':
        tri1s += A3[t,t]/2
        tri2s += TV3[t,t]/2
        tri3s += TTT3[t,t]/2
        
# not 100% sure this is correct, since there are no tri3s, didn't check.
part1 = tri1s - tri2s/2 - tri3s/3 

# https://people.math.ethz.ch/~sudakovb/hidden-clique.pdf
# Alon, Krivelevich, Sudakov: finding a large clique in a random graph
# Basically, look for the vertices with a large entry in the
# 2nd eigenvector of the adjacency matrix

# compute 1st two eigenvectors
l,v = ss.linalg.eigs(A,k=2)

# extract the 2nd eigenvector, attach it to the names, and sort by abs value
vvals = []
for i in range(N):
    vvals.append((abs(v[i,1]),names[i]))
vvals.sort()

# find the biggest entry
bigv,bigs = vvals[-1]

# build the clique by taking all entries that are nearly as large as the bigv
clique = []
for (v,s) in vvals:
    if v > bigv*.9:
        clique.append(s)

print('part1:',part1)

clique.sort()
print('part2:',','.join(clique))
