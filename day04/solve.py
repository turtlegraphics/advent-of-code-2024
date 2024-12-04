# AOC 2024 Day 04
# OK, cheat day - I wrote a word search solver some years ago and
# adapted it for today.  Sadly it was python 2 and I don't have that installed
# so it took me forever to update to python 3.
#

"""
Solves word searches

Given the grid as the first argument and a list of words on stdin.

This finds all locations of the target words in the grid.
It also reports the remaining letters, in order, and gives letter
distributions for the grid and the target words.

You can feed it a dictionary as the target to look for extraneous
words as well.

Bryan Clair 2015-2020
"""

import string

class ANSI:
    """ANSI Foreground Color Escape Codes."""
    BLACK      = '\033[30m'
    RED        = '\033[31m'
    GREEN      = '\033[32m'
    YELLOW     = '\033[33m'
    BLUE       = '\033[34m'
    MAGENTA    = '\033[35m'
    CYAN       = '\033[36m'
    WHITE      = '\033[37m'
    BRIGHTBLUE = '\033[94m'
    ENDC       = '\033[0m'

class Grid:
    """A grid of data that can be searched for runs of data, and marked
       with found runs.
       If the data is characters, this is a wordsearch, and the runs of
       data are the hidden words."""

    def __init__(self,data,colors=True):
        """Create grid from given data.
           If data is a string, open and read data from that file.
           Otherwise, data should be a list of lists (or strings).
           The colors argument is True if you want ANSI color output,
              False if you want blank (.) characters in output."""
        self.colors = colors
        self.grid = []
        for line in open(data):
            self.grid.append(line.strip())

        self.used = [ [0]*len(line) for line in self.grid]

        # Create a dictionary with the letter distribution of the grid.
        self.distribution = Distribution()
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                self.distribution.add(self.grid[r][c])
        
    def usecolors(self,colors):
        """Pass True to use ANSI colors, False to use blanks in output."""
        self.colors = colors

    def find(self,word):
        """
        Find all instances of word in the grid.
        Return a list of tuples (word, startx, starty, dx, dy) of locations.
        """
        found = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == word[0]:
                    for (dx,dy) in [(-1,-1),( 0,-1),( 1,-1),
                                    (-1, 0),        ( 1, 0),
                                    (-1, 1),( 0, 1),( 1, 1)]:
                        i = 0
                        (x,y) = (c,r)
                        try:
                            while self.grid[y][x] == word[i]:
                                x += dx
                                y += dy
                                i += 1
                                if i == len(word):
                                    found.append((word,c,r,dx,dy))
                                    break
                                if x < 0 or y < 0:
                                    break
                        except IndexError:
                            pass
        return found

    def mark_tuples(self,tuples):
        """Mark locations given by a list of tuples
           (word,xstart,ystart,dx,dy)"""
        for (word,x,y,dx,dy) in tuples:
            for c in word:
                self.used[y][x] += 1
                x += dx
                y += dy
        
    def mark(self,word):
        """Find and mark locations of a word."""
        self.mark_tuples(self.find(word))

    def remains(self):
        """Return a string of the unused letters in order."""
        out = ''
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if not self.used[r][c]:
                    out += str(self.grid[r][c])
        return out
        
    def __str__(self):
        """Uses ANSI escape sequences to color the used letters."""
        out = ''
        usecolors = [ANSI.BLACK, ANSI.YELLOW, ANSI.CYAN, ANSI.MAGENTA,
                     ANSI.BLUE, ANSI.BLUE, ANSI.BLUE, ANSI.BLUE, ANSI.BLUE]

        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.used[r][c]:
                    if self.colors:
                        out += usecolors[self.used[r][c]]
                        out += str(self.grid[r][c])
                        out += ANSI.ENDC
                    else:
                        out += '.'
                else:
                    out += str(self.grid[r][c])
            out += '\n'
        return out.strip()

class Distribution:
    """Implement a letter distribution."""
    def __init__(self):
        self.d = {}
        for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.d[c] = 0
            
    def add(self,c):
        self.d[c.upper()] += 1

    def __str__(self):
        key = ''
        count = ''
        for c in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            key += '%3s' % c
            count += '%3d' % self.d[c]
        return key + '\n' + count
        
if __name__=='__main__':
    import sys
    
    # Read grid from filename in command line
    if len(sys.argv) > 1:
        g = Grid(sys.argv[1])
    else:
        g = Grid('input.txt')

    # Read and find words, one per line on stdin
    spots = g.find('XMAS')

    print('part 1',len(spots))

    part2 = 0
    spots = g.find('MAS')
    centers = []
    for (w,x,y,dx,dy) in spots:
        if dx*dy != 0:
            x += dx
            y += dy
            if (x,y) in centers:
                part2 += 1
            else:
                centers.append((x,y))
    print('part 2',part2)
