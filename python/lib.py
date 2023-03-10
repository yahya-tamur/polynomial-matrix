from __future__ import print_function
from functools import reduce
import builtins as __builtin__
from typing import Callable, TypeVar, List
import re

NumPoly = list[int]

def p_trim(a: NumPoly) -> NumPoly:
    for aa in reversed(a):
        if aa == 0:
            del a[-1]
        else:
            break

def p_add(a: NumPoly, b: NumPoly) -> NumPoly:
    ans = a.copy()
    ans.extend([0]*(len(b)-len(a)))
    for (i, bb) in enumerate(b):
        ans[i] += bb
    p_trim(ans)
    return(ans)

def p_mul(a: NumPoly, b: NumPoly) -> NumPoly:
    ans = (len(a)+len(b)-1)*[0]
    for (i,aa) in enumerate(a):
        for (j, bb) in enumerate(b):
            ans[i+j] += aa*bb
    return(ans);

T = TypeVar('T')
M = List[List[T]]
BinOp = Callable[[T,T],T]
EmpOp = Callable[[],T]

# O(n^3) :(
def mat_mul(a: M, b: M, add: BinOp, mul: BinOp, zero: EmpOp) -> M:
    (n,m,o) = len(a), len(b), len(b[0])

    ans = []
    for nn in range(n):
        ans.append([])
        for _ in range(o):
            ans[-1].append(zero())

    for i in range(n):
        for j in range(m):
            for k in range(o):
                ans[i][k] = add(ans[i][k], mul(a[i][j],b[j][k]))
    return ans

NM = list[list[int]]

def nm_mul(a: NM, b: NM) -> NM:
    return mat_mul(a,b,lambda x,y: x+y, lambda x,y:x*y, lambda: 0);

NPM = list[list[NumPoly]]

def pm_mul(a: NPM, b: NPM) -> NPM:
    return mat_mul(a,b,p_add, p_mul, lambda: []);

def pm_print(a: NPM) -> str:
    def st(a,n):
        if a < 0 and n > 0:
            a = -a
        if a == 0:
            return ''
        coef = str(a)
        if n > 0 and a == 1:
            coef = ''
        match n:
            case 0:
                return coef
            case 1:
                return coef + 'x'

        sups = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        ans = ''

        while n != 0:
            ans = sups[n % 10] + ans
            n = n // 10

        return coef + 'x' + ans

    cl = [0 for _ in a[0]]
    ccl = [[] for _ in a[0]]

    s = [[['' for _ in a[i][j]] for j in range(len(a[0]))] for i in range(len(a))]

    for i in range(len(a)):
        for j in range(len(a[0])):
            ccl[j].extend([0]*(len(a[i][j])-len(ccl[j])))
            for k in range(len(a[i][j])):
                ccl[j][k] = max(ccl[j][k], len(st(a[i][j][k],k)))

    for i in range(len(a)):
        for j in range(len(a[0])):
            first = True
            for k in range(len(a[i][j])):
                s[i][j][k] = st(a[i][j][k], k)
                l = len(s[i][j][k])
                if k > 0:
                    if (a[i][j][k] > 0):
                        if not first:
                            s[i][j][k] = ' + ' + s[i][j][k]
                        else:
                            s[i][j][k] = '   ' + s[i][j][k]
                    if (a[i][j][k] == 0):
                        s[i][j][k] = '   ' + s[i][j][k]
                    if (a[i][j][k] < 0):
                        s[i][j][k] = ' - ' + s[i][j][k]
                s[i][j][k] = ' '*(ccl[j][k] - l) + s[i][j][k]
                if (a[i][j][k] != 0):
                    first = False
            s[i][j] = ''.join(s[i][j])
            cl[j] = max(cl[j], len(s[i][j]))

    for i in range(len(a)):
        for j in range(len(a[0])):
            s[i][j] += (cl[j] - len(s[i][j]))*' '
        s[i] = '│ ' + (' │ '.join(s[i])) + ' │\n'

    line = lambda l,m,r: f'{l}─'+f'─{m}─'.join(['─'*n for n in cl])+f'─{r}\n'
    return(line('┌','┬','┐') + line('├','┼','┤').join(s) + line('└','┴','┘'))

interp_re = re.compile(r"(?P<num>-?\d+)|(?P<bar>\.)|(?P<nl>\n|\|)");

def pm_i(s: str) -> NPM :
    init = 0
    while s[init] == '\n':
        init += 1

    ans = [[[]]]

    for mm in re.finditer(interp_re, s[init:]):
        match mm.lastgroup:
            case 'num': ans[-1][-1].append(int(mm.group()))
            case 'bar': ans[-1].append([])
            case 'nl': ans.append([[]])

    for aa in reversed(ans):
        if aa == [[]]:
            del ans[-1]
        else:
            break
    return(ans)

def pm_add(a: NPM, b: NPM) -> NPM:
    return [[p_add(a[i][j],b[i][j]) for j in range(len(a[0]))] for i in range(len(a))]

def pm_scalar(s: NumPoly, a: NPM) -> NPM:
    ans = [[[] for _ in range(len(a[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            ans[i][j] = p_mul(s,a[i][j])
    return ans

def pm_I(n: int) -> NPM:
    return [[[1] if i == j else [] for i in range(n)] for j in range(n)]

def pm_Ix(n: int) -> NPM:
    return pm_scalar([0,1],pm_I(n))

def perms_step(l, rest):
    return [ ([x * ((-1) ** i)] + rest, l[:i] + l[i+1:] ) for i, x in enumerate(l)]

def det3(n) -> []:
    a = n.matrix
    perms = [
        ((0,1,2),1),
        ((0,2,1),-1),
        ((1,2,0),1),
        ((1,0,2),-1),
        ((2,0,1),1),
        ((2,1,0),-1)
    ]
    ans = []

    for (perm, sign) in perms:
        factor = [sign]
        for i in range(3):
            factor = p_mul(factor, a[i][perm[i]])
        ans = p_add(ans, factor)
    return ans



class pm:
    matrix: NPM
    def __init__(self, inp):
        if isinstance(inp, str):
            self.matrix = pm_i(inp)
        else:
            self.matrix = inp

    def __str__(self, ):
        return pm_print(self.matrix)

    def __repr__(self, ):
        return pm_print(self.matrix)

    def __mul__(self, rhs):
        if isinstance(rhs, pm):
            return pm(pm_mul(self.matrix, rhs.matrix))
        return pm(pm_scalar(rhs, self.matrix))

    def __rmul__(self, lhs):
        return self * lhs

    def __add__(self, rhs):
        return pm(pm_add(self.matrix, rhs.matrix))

    def __sub__(self, rhs):
        return pm(pm_add(self.matrix, pm_scalar([-1],rhs.matrix)))

    def __xor__(self, rhs):
        ans = I(len(self.matrix))
        s = self
        while rhs != 0:
            if rhs & 1:
                ans *= s
            s *= s
            rhs //= 2
        return ans

def I(n: int):
    return pm(pm_I(n))

def Ix(n: int):
    return pm(pm_Ix(n))


            
