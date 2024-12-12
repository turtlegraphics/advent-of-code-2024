#
# Advent of Code 2022
# Bryan Clair
#
# Utilities, including:
#   * Argument parsing
#   * Memoization
#        - nope, use @functools.cache or @functools.lru_cache(maxsize=x)
#   * Point classes
#      Point
#      Point3D
#      Turtle
#      HexPoint
#   * Grid classes
#      Grid
#      HexGrid
#   * Number theoretic functions:
#      chinese_remainder theorem
#      mul_inv - multiplicative inverse in modular arithmetic
#   * ZSubset class to effeciently hold arbitrary subsets of the integers
#   
import argparse
import math
import functools
import copy

_verbosity_level = 0

def parse_args():
    """
    Function to parse arguments for an AOC solution.
    Sets input file to input.txt unless otherwise specified.
    Handles part, debug, quiet, verbose flags.
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        action = "count",
                        dest = "verbose",
                        default = 0,
                        help = "Set verbosity level (-v, -vv, -vvv,...)")
    
    parser.add_argument("-q", "--quiet",
                        action = "store_const",
                        const = 0,
                        dest = "verbose",
                        help = "Suppress output.")
    
    parser.add_argument("-d", "--debug",
                        action="store",
                        dest = "debug",
                        default = 0,
                        type = int,
                        help = "Debug level, default 0.")
    
    parser.add_argument("-p", "--part",
                        action="store",
                        dest = "part",
                        default = 1,
                        type = int,
                        help = "Which part of the problem to solve (1 or 2)")
    
    parser.add_argument("file",
                        nargs = "?",
                        default = "input.txt",
                        help = "Problem input file (optional).")
    args = parser.parse_args()

    global _verbosity_level
    _verbosity_level = args.verbose

    return args

def debug(*args,**kwargs):
    """Hacky debug print function."""
    if _verbosity_level > 0:
        print(*args,**kwargs)

class memoized(object):
    def __init__(self, func):
        raise NotImplementedError("@memoized is gone. Use @functools.cache instead.")


# CRT from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python      
def chinese_remainder(n, a):
    """solves the chinese remainder theorem for x == a (mod n)"""
    sum = 0
    prod = functools.reduce(lambda a, b: a*b, n)

    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    """returns the multiplicative inverse of a (mod b)"""
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

class ZSubset:
    """
    Implements a (finite) subset of the integers as a union of ranges.
    Probably better to use a dict if your subset has lots of isolated points,
    but efficient if your subset consists of solid ranges.
    See AOC 2022 Day 15 for a use case.
    """
    def __init__(self,x0=None,x1=None):
        """
        Create a new ZSubset which is either the empty set,
        the point x0, or the set x0,...,x1
        """
        if x0 is None:
            self.ranges = []
        else:
            if x1 is None:
                self.ranges = [[x0,x0]]
            else:
                self.ranges = [[x0,x1]]

    def union(self, other):
        """
        Alters self to become self U other.
        Current implementation is inefficient:
          O(n^2) where n is number of ranges.  Should be O(n).
        """
        for r in other.ranges:
            self._addrange(r)

    def _addrange(self,r):
        """Add a signle range, keeping contiguous ranges"""
        x0,x1 = r
        
        # find the rightmost range with x coordinate less than x0
        try:
            i = 0
            while self.ranges[i][0] < x0:
                i += 1
        except IndexError:
            pass
        if (i == 0) or (x0 > self.ranges[i-1][1]+1):
            self.ranges.insert(i,[x0,x1])
        else:
            i -= 1
            # combine with range[i]
            self.ranges[i][1] = max(self.ranges[i][1],x1)

        # now see if the ith range needs to combine with i+1:
        try:
            while self.ranges[i][1] >= self.ranges[i+1][0]-1:
                self.ranges[i][1] = max(self.ranges[i][1],self.ranges[i+1][1])
                del self.ranges[i+1]
        except IndexError:
            pass

    def display(self):
        if not self.ranges:
            print('<empty set>')
            return

        x = self.ranges[0][0]
            
    def __str__(self):
        out = ''
        for r in self.ranges:
            if r[0]==r[1]:
                # single point range
                out += '['+str(r[0])+']'
            else:
                out += str(r)
            out += ' '
        return out.strip()


class Point:
    """
    A 2d point class
    """
    def __init__(self, x=0, y=0):
        """
        Construct from another point, an (x,y) tuple,
        or x and y passed as values.
        """
        if isinstance(x,Point):
            self.x = x.x
            self.y = x.y
        elif isinstance(x,tuple) or isinstance(x,list):
            self.x, self.y = x
        else:
            self.x, self.y = x,y

    def __copy__(self):
        return Point(self)

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self,other):
        return (self.x == other.x) and (self.y == other.y)

    def __iadd__(self,other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self,other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self,scalar):
        self.x *= scalar
        self.y *= scalar
        return self

    def __itruediv__(self,scalar):
        self.x /= scalar
        self.y /= scalar
        return self

    def __ifloordiv__(self,scalar):
        self.x //= scalar
        self.y //= scalar
        return self
    
    # Everything below here is dimension agnostic and inherited to Point3d
    
    def __ne__(self,other):
        return not self == other

    def __add__(self,other):
        newpt = self.__copy__()
        newpt += other
        return newpt

    def __sub__(self,other):
        newpt = self.__copy__()
        newpt -= other
        return newpt

    def __mul__(self,scalar):
        """Scalar multiplication"""
        newpt = self.__copy__()
        newpt *= scalar
        return newpt

    def __truediv__(self,scalar):
        """Scalar division"""
        newpt = self.__copy__()
        newpt /= scalar
        return newpt

    def __abs__(self):
        """Euclidean length"""
        return math.sqrt(self.length2())

    def dot(self, other):
        return sum([a*b for (a,b) in zip(self,other)])
    
    def length(self):
        """Euclidean length"""
        return abs(self)
        
    def length2(self):
        """Euclidean length squared"""
        return sum([c ** 2 for c in self])
        
    def dist(self, other):
        """Euclidean distance."""
        return abs(self - other)

    def dist2(self,other):
        """Euclidean distance, squared"""
        return (self - other).length2()

    def manabs(self):
        """Manhattan metric (distance from 0)"""
        return sum([abs(c) for c in self])
    
    def mandist(self,other):
        """Manhattan distance"""
        return (self - other).manabs()
    
    def unit(self):
        """Make a new unit vector, same direction."""
        a = abs(self)
        return (self/a).__copy__()

    def __hash__(self):
        return hash(tuple(self))
    
    def __str__(self):
        return str(tuple(self))

class Point3d(Point):
    """
    A 3d point class
    """
    def __init__(self, x=0, y=0, z=0):
        """
        Construct from another point, an (x,y,z) tuple,
        or x y z passed as values.
        """
        if isinstance(x,Point3d):
            self.x = x.x
            self.y = x.y
            self.z = x.z
        elif isinstance(x,tuple) or isinstance(x,list):
            self.x, self.y, self.z = x
        else:
            self.x, self.y, self.z = x,y,z

    def __copy__(self):
        return Point3d(self)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __eq__(self,other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __iadd__(self,other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self,other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __imul__(self,scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self

    def __itruediv__(self,scalar):
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return self

    def cross(self,b):
        return Point3d(self.y*b.z - self.z*b.y,
                       self.z*b.x - self.x*b.z,
                       self.x*b.y - self.y*b.x)
    
class Turtle(Point):
    """A point that can move like a turtle."""
    def __init__(self,*args, **kwargs):
        Point.__init__(self,*args, **kwargs)
        self.heading = None
        
    def forward(self,dist):
        self += self.heading*dist

    def back(self,dist):
        self -= self.heading*dist

    def face(self,heading):
        self.heading = self._compass[heading]

    def left(self):
        """Turn left 90."""
        self.heading = Point(-self.heading.y, self.heading.x)
        
    def right(self):
        """Turn right 90."""
        self.heading = Point(self.heading.y, -self.heading.x)
        
    _compass = {'N':Point(0,1), 'W':Point(-1,0), 'S':Point(0,-1), 'E':Point(0,1)}

    
class Grid:
    """
    A 2d grid of tile objects (probably characters) that can be any size.
    Coordinates are tuples (x,y) or Points.
    Keeps track of its own dimensions and displays the smallest rectangle that
    contains all data.
    """
    def __init__(self, orig = None):
        if orig:
            self.raster = copy.deepcopy(orig.raster)
            self.xmin = orig.xmin
            self.xmax = orig.xmax
            self.ymin = orig.ymin
            self.ymax = orig.ymax
        else:
            self.raster = {}
            self.xmin = None
            self.xmax = None
            self.ymin = None
            self.ymax = None
        
    def __setitem__(self,p,tile):
        x,y = p

        if self.raster:
            self.xmin = min(self.xmin,x)
            self.xmax = max(self.xmax,x)
            self.ymin = min(self.ymin,y)
            self.ymax = max(self.ymax,y)
        else:
            self.xmin = x
            self.xmax = x
            self.ymin = y
            self.ymax = y

        self.raster[(x,y)] = tile

    def __getitem__(self,p):
        x,y = p
        return self.raster[(x,y)]

    def __contains__(self,p):
        x,y = p
        return (x,y) in self.raster

    def pop(self,p):
        return self.raster.pop(p)
    
    def __iter__(self):
        return iter(self.raster)

    def _neighbors(self, p, dirs, validate):
        """Return a list of neighbors of p in dirs directions.
        * Returns only neighbors present in the grid if validate==True
        * Returns all possible neighbors if validate==False
        """
        n = []
        for d in dirs:
            q = p + Point(d)
            if (not validate) or q in self:
                n.append(q)
        return n

    _dirs = [(1,0),(-1,0),(0,1),(0,-1),
             (1,1),(-1,1),(1,-1),(-1,-1)]

    def neighbors(self, p, diagonal = False, validate = True):
        """
        * Returns only neighbors present in the grid if validate==True
        * Returns all possible neighbors if validate==False

        Uses the four cardinal directions, unless diagonal is True,
        in which case it uses the eight grid neighbors
        """
        x,y = p
        if diagonal:
            return self._neighbors(Point((x,y)),self._dirs,validate)
        return self._neighbors(Point((x,y)),self._dirs[:4],validate)

    def bounds(self):
        """Return bounds of the grid in format (xmin, ymin, xmax, ymax)"""
        return (self.xmin,self.ymin,self.xmax,self.ymax)

    def width(self):
        """Return the max width of the grid."""
        return self.xmax - self.xmin + 1
    
    def height(self):
        """Return the max height of the grid."""
        return self.ymax - self.ymin + 1
    
    def scan(self,map,vflip=True):
        """
        Take a list of strings or lists (map) and scan into the grid.

        If vflip is True, the first line of map is at positive y and
        the last line of map is at y=0.  For a map coming from a text file,
        this is probably what you want.

        If vflip is False, the first line of map is at y=0 and the lines
        proceed upwards from there.
        """
        for y,row in enumerate(reversed(map) if vflip else map):
            for x,v in enumerate(list(row)):
                self[(x,y)] = v

    def dijkstra(self, source, target = None,
                 distance_function = lambda u,v : 1):
        """
        Perform Dijkstra's algorithm to find the distance of all Grid points
        from the source.

        Returns a pair (dist, prev) of dictionaries which give the distance
        from source for each point, and the prev point in the distance digraph.
        So you can follow the prev links back to the source.

        * If the grid is disconnected, it stops when the connected component
        is fully mapped out.  In other words, dist[p] exists if and only if
        p is in the connected component of source.

        * Stops if target is reached and just return a partial result, in
        particular dist[target] will be the distance from source to target,
        and you can follow the prev[] path backwards.

        * distance_function can weight edges in the graph, by returning
        the weight/distance from u to v. If it returns None, there is no
        path from u to v.
        """

        sx,sy = source
        source = (sx,sy)

        assert(source in self)
        
        dist = {}
        prev = {}
        Q = set()
        Q.add(source)
        dist[source] = 0
        prev[source] = None
        visited = set()
        
        while Q:
            # find min distance point u
            min_dist = float("inf")
            for p in Q:
                if dist[p] < min_dist:
                    min_dist = dist[p]
                    u = p

            if u == target:
                return (dist, prev)
            
            Q.remove(u)
            visited.add(u)
            
            # update u's neighbors
            nbrs = self.neighbors(u)
            for v in nbrs:
                v = (v.x,v.y)
                if v in visited:
                    continue
                distuv = distance_function(u,v)
                if distuv is None:
                    continue
                dv = dist[u] + distuv
                if v in Q:
                    if dv < dist[v]:
                        dist[v] = dv
                        prev[v] = u
                else:
                    Q.add(v)
                    dist[v] = dv
                    prev[v] = u

        return (dist, prev)

    def region(self,origin):
        """
        Find all points in a connected region tha have the same value.
        """
        def sameval(u,v):
            if self[u] == self[v]:
                return 1
        (dist,prev) = self.dijkstra(origin,target=None,
                                    distance_function = sameval)
        return list(dist.keys())

    def perimeter(self,region):
        """
        Return the straight-line perimeter of a region.
            +-+-+-+-+
            |A A A A|
            +-+-+-+-+     +-+
                          |D|
            +-+-+   +-+   +-+
            |B B|   |C|
            +   +   + +-+
            |B B|   |C C|
            +-+-+   +-+ +
                      |C|
            +-+-+-+   +-+
            |E E E|
            +-+-+-+
        A has 10, B has 8, C has 10, D has 4, E has 8.
        (see AoC 2024 day 12)
        """
        perim = 0
        val = self[region[0]]
        for q in region:
            for n in self.neighbors(q,validate=False):
                try:
                    if self[n] != val:
                        perim += 1
                except KeyError:
                    perim += 1
        return perim

    def sides(self,region):
        """
        Return the number of sides of a region.
        Equivalently, return the number of corners.
            +-+-+-+-+
            |A A A A|
            +-+-+-+-+     +-+
                          |D|
            +-+-+   +-+   +-+
            |B B|   |C|
            +   +   + +-+
            |B B|   |C C|
            +-+-+   +-+ +
                      |C|
            +-+-+-+   +-+
            |E E E|
            +-+-+-+
        A, B, D, E have 4.  C has 8.
        (see AoC 2024 day 12)
        """
        val = self[region[0]]
        corners = 0
        for (x,y) in region:
            for dx in [-1,1]:
                for dy in [-1,1]:
                    try:
                        valx = (self[x+dx,y] == val)
                    except KeyError:
                        valx = False

                    try:
                        valy = (self[x,y+dy] == val)
                    except KeyError:
                        valy = False

                    try:
                        valz = (self[x+dx,y+dy] == val)
                    except KeyError:
                        valz = False

                    if (not valz) and valx and valy:
                        # inside corner
                        corners += 1

                    if (not valx) and (not valy):
                        # outside corner
                        corners += 1
        return corners

    def __str__(self):
        """Calls display with defaults."""
        return self._display(' ',False,'')
    
    def display(self, blank=' ', vflip = False, sep=''):
        """
        Display the grid in a customizable manner.
        
        Always shows a rectangle which is exactly large enough to
        contain all cells with data.
        
        Blank cells are displayed with a space, unless blank is set.
        
        By default, higher the y axis increases upwards, like in math.
        If vflip is True, the y axis increases downwards.
        
        sep is put between each cell
        """
        print(self._display(blank, vflip, sep))
        
    def _display(self, blank, vflip, sep):
        result = ''
        if vflip:
            rows = range(self.ymin, self.ymax+1)
        else:
            rows = range(self.ymax,self.ymin-1,-1)

        for y in rows:
            out = ''
            for x in range(self.xmin,self.xmax + 1):
                if out:
                    out += sep
                if (x,y) in self.raster:
                    out += str(self.raster[(x,y)])
                else:
                    out += blank
            if result != '':
                result += '\n'
            result += out

        return result
    
class HexGrid(Grid):
    """
    Class representing a hexagonal grid.
    See HexPoint class for details of coordinates
    """
    def neighbors(self, p, validate=True):
        """
        * Returns only neighbors present in the grid if validate==True
        * Returns all possible neighbors if validate==False

        p must be a HexPoint
        """
        return self._neighbors(p,p.DIRECTIONS.values(),validate)

    def display(self):
        for y in range(self.ymax,self.ymin-1,-1):
            out = ' '*(y-self.ymin)
            for x in range(self.xmin,self.xmax + 1):
                if (x,y) in self.raster:
                    out += str(self.raster[(x,y)])
                else:
                    out += ' '
                out += ' '
            print(out)

class HexPoint(Point):
    """
    Class for working with coordinates on a hexagonal grid.
    Coordinates are mappped to (x,y) with connections made in this way:
      NW  NE
     W  *   E
      SW  SE
    """
    DIRECTIONS = {
        'ne' : (0,1),
        'sw' : (0,-1),
        'nw' : (-1,1),
        'se' : (1,-1),
        'w' : (-1,0),
        'e' : (1,0)
        }
        
    def __copy__(self):
        return HexPoint(self)

    def __abs__(self):
        """Returns distance to the origin on the hex grid"""
        x,y = self.x,self.y
        diag = 0
        if (x > 0 and y < 0):
            diag = -min(abs(x),abs(y))
        if (x < 0 and y > 0):
            diag = min(abs(x),abs(y))
        return abs(diag) + abs(x + diag) + abs(y - diag)

    def move(self,dir):
        self += HexPoint(self.DIRECTIONS[dir.lower()])

if __name__ == '__main__':
    # Argument parsing
    print('-'*20)
    print('Argument parsing')
    print('-'*20)
    args = parse_args()
    print(args)
    if args.verbose == 0:
        print('Verbose level 0, use -v,-vv,... to change')
    else:
        debug('Verbose level',args.verbose)
    print()
        
    # Progress bar
    # Requires tqdm and I don't want that to cause installation problems (which it did)
    #print('-'*20)
    #print("Progress bar")
    #print('-'*20)
    #from time import sleep
    #for i in tqdm(range(75)):
    #    sleep(0.01)
    #print()

    # Memoization
    print('-'*20)
    print("Memoization using @functools.cache")
    print('-'*20)
    import functools
    @functools.cache
    def fibonacci(n):
        if n < 2:
            return 1
        return fibonacci(n-1) + fibonacci(n-2)
    print('Fibonacci 100 =',fibonacci(100))
    
    # Number Theory
    print('-'*20)
    print("Number Theory")
    print('-'*20)
    print('The multiplicative inverse of 5 mod 13 is',mul_inv(5,13))
    print('Solve x = 4 mod 16 and x = 2 mod 21:',)
    print(chinese_remainder([16,21],[4,2]))

    # ZSubset
    print('-'*20)
    print("ZSubset")
    print('-'*20)
    empty = ZSubset()
    A = ZSubset(0,10)
    B = ZSubset(11)
    C = ZSubset(15,20)
    D = ZSubset(-4,19)
    empty.display()
    print('A=',A)
    print('B=',B)
    print('C=',C)
    print('D=',D)
    A.union(C)
    A.union(B)
    print('A U B U C =',A)
    A.union(D)
    print('A U B U C U D =',A)
    
    # Point
    print('-'*20)
    print("Point class")
    print('-'*20)
    p = Point(1,2)
    q = Point((3,3)) # ok to use tuple
    r = Point(p)
    r += Point(10,10)
    r -= Point(5,1)

    print('p=%s,q=%s,r=%s' % (str(p),str(q),str(r)))
    print('p and q are',p.dist(q),'apart')
    print('p + q = ',p+q)
    print('r - q = ',r-q)
    print('3p - 2q =', p*3 - q*2)
    assert(r - q == Point(3,8))
    assert(p != q)

    # Point 3d
    print('-'*20)
    print("Point3d class")
    print('-'*20)
    p = Point3d(1,2,3)
    q = Point3d(-1,5,2)
    r = Point3d(0,0,0)
    print('p=%s,q=%s,r=%s' % (str(p),str(q),str(r)))
    print('p and q are',p.dist(q),'apart')
    print('p + q = ',p+q)
    print('r - q = ',r-q)
    print('p . q = ',p.dot(q))
    assert(r - q == Point3d(1,-5,-2))
    assert(p != q)

    # Turtle
    print('-'*20)
    print("Point3d class")
    print('-'*20)
    g = Grid()
    g.scan(['....']*4)
    t = Turtle()
    t.face('N')
    g[t] = '1'
    t.forward(1)
    g[t] = '2'
    t.right()
    t.forward(3)
    g[t] = '3'
    t.left()
    t.forward(1)
    g[t] = '4'
    t.left()
    t.forward(2)
    g[t] = '5'
    t.right()
    t.forward(1)
    g[t] = '6'
    g.display()

    # Grid
    print('-'*20)
    print("Grid class")
    print('-'*20)
    g = Grid()
    g.bounds()
    g[Point(-1,0)] = 'o'
    g[Point(1,0)] = 'o'
    dots = [(-1,2),(0,2),(1,2),(-2,1),(-2,0),(-2,-1),
            (2,1),(2,0),(2,-1),(-1,-2),(0,-2),(1,-2)]
    for p in dots:
        g[p] = '*'
    nose = Point(0,-1)
    g[nose] = 'U'
    print(g)

    dotcount = 0
    for p in g:
        if g[p] == '*':
            dotcount += 1
    print('There are %d stars.' % dotcount)
    assert(dotcount == len(dots))

    assert(g[nose] == 'U')
    assert((5,5) not in g)
    assert((2,0) in g)

    nosenbrs = tuple([len(g.neighbors(nose,diag)) for diag in [False,True]])
    print('nose U has %d cardinal and %d diagonal neighbors.' % nosenbrs)
    assert((1,5) == nosenbrs)

    print('here it is upside down and shaded in with .s')
    g.display(blank='.', vflip=True)

    print('here it is in jail')
    g.display(sep='|')

    print('now lets print a little xmas art')
    sleighart = r"""
__     _  __ 
| \__ `\O/  `--  {}    \}    {/
\    \_(~)/______/=____/=____/=*
 \=======/    //\\  >\/> || \> 
----`---`---  `` `` ```` `` ``""".split('\n')
    sleigh = Grid()
    sleigh.scan(sleighart)
    print(sleigh)
    print('xmin,ymin,xmax,ymax =',sleigh.bounds())

    print()
    print('solve a maze')
    mazeart = """\
.--.--.--.--.--.--.
|     |        |  |
:  :--:  :  :  :  :
|  |     |  |     |
:  :  :  :--:--:--:
|  |  |           |
:  :  :--:--:--:  :
|  |        |E |  |
:  :--:--:  :  :  :
|     |     |  |  |
:--:  :  :--:  :  :
|S       |        |
:--:--:--:--:--:--:
""".split('\n')
    maze = Grid()
    maze.scan(mazeart)
    for p in maze:
        if maze[p] == 'S':
            maze_start = p
        if maze[p] == 'E':
            maze_end = p
    print(maze)
    maze[maze_start] = ' '
    maze[maze_end] = ' '
    
    def nowall(u,v):
        if maze[u] == ' ' and maze[v] == ' ':
            return 1
        else:
            return None

    dist, prev = maze.dijkstra(source = maze_start, target = maze_end,
                               distance_function = nowall)

    print('distance to finish:',dist[maze_end])
    solution = Grid()
    for p in maze:
        solution[p] = maze[p]
    p = maze_end
    while p:
        solution[p] = str(dist[p])[-1]
        p = prev[p]
    print(solution)

    # Regions
    print()
    print('Region handling')
    OXmap = """\
AAAA..
A..A..
AAA...
B.BBBB
BBB...""".split('\n')
    OX = Grid()
    OX.scan(OXmap)
    print(OX)
    print("  The grid has regions A and B (and some .'s)")
    regionA = OX.region(origin=(0,2))
    regionB = OX.region(origin=(0,0))
    print("  %c has area %d, perimeter %d, and %d sides/corners." %
          ('A', len(regionA), OX.perimeter(regionA), OX.sides(regionA)))
    print("  %c has area %d, perimeter %d, and %d sides/corners." %
          ('B', len(regionB), OX.perimeter(regionB), OX.sides(regionB)))
    
    # HexGrid, HexPoint
    print('-'*20)
    print("HexGrid, HexPoint")
    print('-'*20)
    print('Distances from origin:')
    h = HexGrid()
    for x in range(-3,4):
        for y in range(-3,4):
            p = HexPoint(x,y)
            h[p] = str(abs(p))

    h.display()

    h = HexGrid()
    for x in range(-5,4):
        for y in range(-2,6):
            h[(x,y)] = '.'

    print()
    print('Take a stroll')
    p = HexPoint()
    q = HexPoint()
    q.move('sw')
    q.move('sw')
    q.move('w')
    h[q] = 'q'

    i = 0
    h[p] = '0'
    for d in ['e','ne','ne','nw','w','w','w','sw','se']:
        print('%s --%s-->' % (str(p),d),)
        p.move(d)
        i += 1
        h[p] = str(i)
    print(p)

    h.display()

    print('Ended',abs(p),'from start')
    print('Ended',p.dist(q),'from q')

    assert(p.dist(q) == 3)
    assert(len(h.neighbors(p)) == 6)
    assert(len(h.neighbors(p,validate=False)) == 6)

