import scipy.sparse as ss
inputlines = [x.strip() for x in open("input.txt").readlines()]

#
# Build list of vertices
#
verts = set()
for line in inputlines:
    sx,sy = line.split('-')
    verts.add(sx)
    verts.add(sy)

verts = list(verts)
N = len(verts)

#
# Build three adjacency matrices
#
A = ss.lil_array((N,N)) # all edges
TV = ss.lil_array((N,N)) # only edges connecting with T vertices
TTT = ss.lil_array((N,N)) # only T vertice and edges between them

for line in inputlines:
    sx,sy = line.split('-')
    x = verts.index(sx)
    y = verts.index(sy)

    # adjacency matrix A for full graph
    A[x,y] = 1
    A[y,x] = 1

    # adjacency matrix TV for subgraph with t-vertices and their edges
    if sx[0] == 't' or sy[0] == 't':
        TV[x,y] = 1
        TV[y,x] = 1

    # adjacency matrix TTT for induced subgraph only containing t-vertices
    if sx[0] == 't' and sy[0] == 't':
        TTT[x,y] = 1
        TTT[y,x] = 1

#
# part 1
#

# count the number of times a tx appears in a triangle,
# the number of times it appears in a triangle with another ty,
# and the number of times it appears in a fully t triangle
A3 = A.dot(A).dot(A)
TV3 = TV.dot(TV).dot(TV)
TTT3 = TTT.dot(TTT).dot(TTT)

tri1s, tri2s, tri3s = 0,0,0

for t,s in enumerate(verts):
    if s[0] == 't':
        tri1s += A3[t,t]/2
        tri2s += TV3[t,t]/2
        tri3s += TTT3[t,t]/2

part1 = tri1s - tri2s/2 - tri3s/3 


#
# part 2
#

# https://people.math.ethz.ch/~sudakovb/hidden-clique.pdf
# Alon, Krivelevich, Sudakov: finding a large clique in a random graph
# Basically, look for the vertices with a large entry in the
# 2nd eigenvector of the adjacency matrix

# compute 1st two eigenvectors
l,v = ss.linalg.eigs(A,k=2)

# extract the 2nd eigenvector, attach it to the names, and sort by abs value
vvals = []
for i in range(N):
    vvals.append((abs(v[i,1]),verts[i]))
vvals.sort()

# find the biggest entry
bigv,bigs = vvals[-1]

# build the clique by taking all entries that are nearly as large as the bigv
clique = []
for (v,s) in vvals:
    if v > bigv*.9:
        clique.append(s)
clique.sort()
part2 = ','.join(clique)

print('part1:',part1)
print('part2:',part2)
