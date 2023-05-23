import math
import itertools
import numpy as np
from scipy.linalg import solve

methods_dict_help = ['simplex', 'brute']

def get_canonical_form(file):

    with open(file) as f:
        eq = [line.strip().split() for line in f.readlines()]

    m, n = map(int, eq[0])
    w = {idx:(-1.0 if sign[0] == ">=" else 1.0) for idx, sign in enumerate(eq[2:-1]) if sign[0] != '='}
    print(w)
    x_unsign = [x for x in range(n) if x+1 not in map(int, eq[-1])]

    A = []
    b = [0]*m
    for idx, eql in enumerate(eq[2:-1]):
        A.append(list(map(float, eql[1:-1])))
        A[idx] += [-A[idx][x] for x in x_unsign]
        ws = [(0.0 if idx != i else w[idx]) for i in w.keys()]
        A[idx] += ws
        
        b[idx] = float(eql[-1])
    

    # коэффитсиент направления
    dir_coef = -1 if eq[1][0] == 'max' else 1
    
    # заполняем вектор c
    c = list(map(float, eq[1][1:]))
    c += [-c[x] for x in x_unsign] + [0] * len(w)
    c = [dir_coef*x for x in c]      

    return (c, A, b)


def brute(c, A, b):
    print(A, b, c)
    basics = itertools.combinations(list(range(len(A[0]))), len(A))
    count = 0
    min_val = None
    res_vector = None
    for basice in basics:
        sub_A = build_sub_matrix(A, basice)
        if get_det(sub_A) != 0:
            x = t(list(solve(np.array(sub_A), np.array(t([b])))))[0]
            if any(xi < 0 for xi in x) == False:
                res = [0]*len(A[0])
                for i, j in zip(basice, x):
                    res[i] = j
                
                val = sum([i*j for i, j in zip(c, res)])
                if min_val is None:
                    print(val)
                    min_val = val
                    res_vector = res
                elif val < min_val:
                    min_val = val
                    print(val)
                    res_vector = res
    return res_vector


def get_det(A):
    if len(A) == 1:
        return A[0][0]

    res = 0
    for i in range(len(A)):
        res += ((-1)**i)*A[0][i]*get_det([line[:i] + line[i+1:] for line in A[1:]])
    
    return res


def gauss(A_const, b_const):
    a = np.array(A_const)
    b = np.array(b_const)
    n = len(b)
    # Elimination phase
    for k in range(0, n-1):
        for i in range(k+1,n):
            if a[i, k] != 0.0:
                #if not null define λ
                lam = a[i,k] / a[k,k]
                #we calculate the new row of the matrix
                a[i,k+1:n] = a[i,k+1:n] - lam*a[k,k+1:n]
                #we update vector b
                b[i] = b[i] - lam*b[k]
                # backward substitution
    for k in range(n-1,-1,-1):
        b[k] = (b[k] - np.dot(a[k,k+1:n],b[k+1:n]))/a[k,k]
    
    return list(b)


def build_sub_matrix(A, indexes):
    return [[line[i] for i in indexes] for line in A]


def mm(matrix_a: list[list[float]], matrix_b: list[list[float]]) -> list[list[float]]:
    """Матричное умножение"""
    res_matrix = [[sum([matrix_a[j][k]*matrix_b[k][i] for k in range(len(matrix_b))]) for i in range(len(matrix_b[0]))] for j in range(len(matrix_a))]

    return res_matrix


def t(matrix: list[list[float]]) -> list[list[float]]:
    """Транспонирование матритсы"""
    t_matrix = [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

    return t_matrix


def simplex(c, A, b):
    table = get_table(c, A, b)
    while can_be_better(table):
        out_col, in_col = get_new_basice(table)
        pivot(out_col, in_col, table)


    print(table)


def get_table(c, A, b):
    """Строим симплекс-таблитсу из исходной ЗЛП"""
    equals = [equal_i + [b_i] for equal_i, b_i in zip(A, b)]
    table = equals + [c + [0]]

    return table


def can_be_better(table):
    """Проверяем оптимальность"""
    c = table[-1]
    return any(x < 0 for x in c)


def get_new_basice(table):
    """Получаем следующий базис"""
    c = table[-1]
    # номер столбца входящего в базис
    in_col = next(i for i, x in enumerate(c) if x < 0)
    # номер выходящего
    candidates = []
    for eq in table[:-1]:
        el = eq[in_col]
        candidates.append(math.inf if el <= 0 else eq[-1]/el)
    
    out_col = candidates.index(min(candidates))

    return out_col, in_col


def pivot(out_col, in_col, table):
    pass


brute(*get_canonical_form('task1.txt'))

# methods_dict = {
#     'first': first_order,
#     'second': second_order,
# }
