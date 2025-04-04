def arrow(F, E, C, A):
    return F == E + C + A

def yellow(B, C, D, E, F):
    return B + C + D + E + F == 10 * B + C and len(set([B, C, D, E, F])) == 5

def sudokuarrow(F, E, C, A):
    return len(set([F, E, C, A])) == 4



"""
_A
BC
DE
_F

B = 1 or 2
F = 6, 7, 8, or 9
A, C, E = 1, 2, 3, 4, 5, 6
"""
As = set()
Bs = set()
Cs = set()
Ds = set()
Es = set()
Fs = set()
sols = []
for A in range(1, 7):
    for B in range(1, 3):
        for C in range(1, 7):
            if C != 6:
                continue
            for D in range(1, 10):
                for E in range(1, 7):
                    for F in range(6, 10):
                        if arrow(F, E, C, A) and yellow(B, C, D, E, F) and sudokuarrow(F, E, C, A):
                            print(f"_{A}\n{B}{C}\n{D}{E}\n_{F}\n\n")
                            As.add(A)
                            Bs.add(B)
                            Cs.add(C)
                            Ds.add(D)
                            Es.add(E)
                            Fs.add(F)
                            sols.append(set([B, C, D, E, F]))

union_of_sols = set().union(*sols)
print(f"Union of all sets in sols: {sorted(union_of_sols)}")

print(f"As: {sorted(As)}")
print(f"Bs: {sorted(Bs)}")
print(f"Cs: {sorted(Cs)}")
print(f"Ds: {sorted(Ds)}")
print(f"Es: {sorted(Es)}")
print(f"Fs: {sorted(Fs)}")