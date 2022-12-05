import urllib.request as u, ssl, numpy as n

def mx(z, m):
    try:
        return max(z, m)
    except:
        return m

def a(L, x, y, m):
    return mx(n.prod([int(L[x][y+i]) for i in range(4)]), m)

def b(L, x, y, m):
    return mx(n.prod([int(L[x+i][y]) for i in range(4)]), m)

def c(L, x, y, m):
    return mx(n.prod([int(L[x+i][y+i]) for i in range(4)]), m)

def d(L, x, y, m):
    return mx(n.prod([int(L[x+i][y-i]) for i in range(4)]), m)

ssl._create_default_https_context = ssl._create_unverified_context
e ="http://cs.carleton.edu/faculty/dln/placement/grid.txt"
f = u.urlopen(e)
L = []

for l in f: L.append(str(l).replace("b'","").replace("\\n","").replace("  "," ").replace("  ", " ").strip().split(" "))
f.close()

m = 1
for x in [int(L[0][i]) for i in range(4)]: m = m*x 
for y in range(len(L)):
    for x in range(len(L[0])):
        m = max(d(L, x, y, m), c(L, x, y, m), b(L, x, y, m), a(L, x, y, m))
print(m)