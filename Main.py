from Input import Input
from Matrix_Utils import Matriz
import random

def generateBxNx(num_vars, num_constraints, a, c, b_xs = None, n_xs = None):
    
    if b_xs is None and n_xs is None:      
        # x_s = list(range(1, num_vars + num_constraints + 1))
        # b_xs = random.sample(x_s, num_constraints)
        # b_xs.sort()
        # n_xs = [x for x in x_s if x not in b_xs]
        # n_xs.sort()
        b_xs = [3, 4, 5]
        n_xs = [1, 2]

    b_x = []
    for i in range(len(a)):
        b_row = []
        for index in b_xs:
            b_row.append(a[i][index - 1]) 
        b_x.append(b_row)

    n_x = []
    for i in range(len(a)):
        n_row = []
        for index in n_xs:
            n_row.append(a[i][index - 1])
        n_x.append(n_row)
        
    cb = [c[i - 1] for i in b_xs]
    cn = [c[i - 1] for i in n_xs]

    return b_xs, n_xs, b_x, n_x, cb, cn

def basic_solution_calc(bx, b):
    xb_aprox = bx.inversa().__mul__(b.transpose())
    xn_aprox = [0] * len(b.mat)
    return xb_aprox, xn_aprox

def relative_cost(bx, nx, cb, cn):
    bx_inverse = bx.inversa()
    lamb = cb.__mul__(bx_inverse)
    print("Multiplicador Simplex:")
    print(lamb.mat)
    print()
    nx_t = nx.transpose()
    ax = [Matriz(i).transpose() for i in nx_t.mat]
    cnx= [cn.mat[0][i] - lamb.__mul__(ax[i]).mat[0][0] for i in range(len(cn.mat[0]))]
    print("Custos Relativos:")
    print(cnx)
    print()
    return cnx

def simplex_direction_calc(nx, bx, index_min):
    ax = nx.transpose().mat[index_min]
    y = bx.inversa().__mul__(Matriz(ax).transpose())
    print("Vetor y")
    print(y.mat)
    print()
    return y

def det_step_var_to_leave_the_base(y, xb, xn, base_new, xb_aprox):
    eps_aux = []
    index_aux = []
    for i in range(len(xb)):
        if y.mat[i][0] > 0:
            eps_aux.append(xb_aprox.mat[i][0]/y.mat[i][0])
            index_aux.append(i)
    eps = min(eps_aux)
    index_eps = index_aux[eps_aux.index(eps)]
    swap_aux = xn[base_new - 1]
    xn[base_new - 1] = xb[index_eps]
    xb[index_eps] = swap_aux
    print(xn)
    print(xb)
    return xb, xn
 
def simplex(a, b, c, num_vars, num_constraints):
    xb, xn, bx, nx, cb, cn = generateBxNx(num_vars, num_constraints, a, c)
    while True:
        print("Básica e não-básica")
        print(f"Matriz B básica: {bx}")
        print(f"Matriz N não-básica: {nx}")
        print(f"Vetor de indices básicos: {xb}")
        print(f"Vetor de indices não-básicos: {xn}")
        print()
        bx = Matriz(bx)
        nx = Matriz(nx)
        cb = Matriz(cb)
        cn = Matriz(cn)
        xb_aprox, xn_aprox = basic_solution_calc(bx, b)
        print("Xb e Xn aproximados:")
        print(xb_aprox.mat)
        print(xn_aprox)
        print()
        cnx = relative_cost(bx, nx, cb, cn)
        min_cnx = min(cnx)
        if min_cnx >= 0:
            z = sum([xb_aprox.mat[i][0] * cb.mat[0][i] for i in range(len(cb.mat[0]))])
            print(z)
            return z
        else:
            index_min = cnx.index(min_cnx)
            base_new = xn[index_min]
            print("Entra na base:")
            print(base_new)
            y = simplex_direction_calc(nx, bx, index_min)
            xb, xn = det_step_var_to_leave_the_base(y, xb, xn, base_new, xb_aprox)
            
            xb, xn, bx, nx, cb, cn = generateBxNx(num_vars, num_constraints, a, c, xb, xn)

def main():
    input = Input("Inputs/inputs1.txt")
    input.read()
    c, a, b = input.getInputs()
    print("Entrada:")
    print(f"Vetor Custo: {c}")
    print(f"Matriz a:{a}")
    print(f"Vetor de termos independentes: {b}")
    print()
    num_vars, num_constraints = input.getNumVars()
    b = Matriz(b)
    z = simplex(a, b, c, num_vars, num_constraints)
    
if __name__ == '__main__':
    main()