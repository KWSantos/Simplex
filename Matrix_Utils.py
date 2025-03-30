def matrix_product(a, b):
    if len(a[0]) != len(b):
        return None

    c = []
    for i in range(len(a)):
        row = []
        for j in range(len(b[0])):
            sum_product = 0
            for k in range(len(a[0])):
                sum_product += a[i][k] * b[k][j]
            row.append(sum_product)
        c.append(row)
    return c


def determinant(matriz):
    n = len(matriz)
    m = len(matriz[0])

    if n != m:
        return None

    if n == 1:
        return matriz[0][0]

    if n == 2:
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

    if n == 3:
        return sarrus(matriz)

    det = 0
    for col in range(n):
        submatriz = []
        for i in range(1, n):
            submatriz.append([matriz[i][j] for j in range(n) if j != col])
        sinal = (-1) ** col
        cofator = sinal * determinant(submatriz)
        det += matriz[0][col] * cofator

    return det


def sarrus(a):
    if len(a) != 3 or any(len(row) != 3 for row in a):
        return None

    pos = (a[0][0] * a[1][1] * a[2][2] +
           a[0][1] * a[1][2] * a[2][0] +
           a[0][2] * a[1][0] * a[2][1])

    neg = (a[0][2] * a[1][1] * a[2][0] +
           a[0][0] * a[1][2] * a[2][1] +
           a[0][1] * a[1][0] * a[2][2])

    return pos - neg


def inverse_matrix(a):

    if determinant(a) == 0:
        return None

    n = len(a)
    for row in a:
        if len(row) != n:
            return None

    identity = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    augmented = [row[:] + identity[i] for i, row in enumerate(a)]

    for col in range(n):
        pivot = augmented[col][col]
        if pivot == 0:
            for r in range(col + 1, n):
                if augmented[r][col] != 0:
                    augmented[col], augmented[r] = augmented[r], augmented[col]
                    break
            else:
                return None

            pivot = augmented[col][col]

        for j in range(col, 2 * n):
            augmented[col][j] /= pivot

        for i in range(n):
            if i != col and augmented[i][col] != 0:
                factor = augmented[i][col]
                for j in range(col, 2 * n):
                    augmented[i][j] -= factor * augmented[col][j]

    inverse = [row[n:] for row in augmented]

    return inverse
