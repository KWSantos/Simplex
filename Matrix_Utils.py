class Matriz():
    def __init__(self, mat):
        if all(isinstance(x, (int, float)) for x in mat):
            mat = [mat]

        self.mat = mat
        self.lin = len(mat)
        self.col = len(mat[0]) if self.lin > 0 else 0

    def getLinha(self, n):
        return [i for i in self.mat[n]]

    def getColuna(self, n):
        return [i[n] for i in self.mat]

    def __mul__(self, mat2):
        if self.col != mat2.lin:
            raise ValueError("Número de colunas da primeira matriz deve ser igual ao número de linhas da segunda matriz.")
        matRes = []

        for i in range(self.lin):
            matRes.append([])

            for j in range(mat2.col):
                listMult = [x * y for x, y in zip(self.getLinha(i), mat2.getColuna(j))]
                matRes[i].append(sum(listMult))

        return Matriz(matRes)

    def determinante(self):
        matriz = self.mat
        n = self.lin
        m = self.col

        if n != m:
            return None

        if n == 1:
            return matriz[0][0]

        if n == 2:
            return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

        if n == 3:
            return self._sarrus()

        det = 0
        for col in range(n):
            submatriz = []
            for i in range(1, n):
                submatriz.append([matriz[i][j] for j in range(n) if j != col])
            sinal = (-1) ** col
            cofator = sinal * Matriz(submatriz).determinante()
            det += matriz[0][col] * cofator

        return det

    def _sarrus(self):
        a = self.mat
        if len(a) != 3 or any(len(row) != 3 for row in a):
            return None

        pos = (a[0][0] * a[1][1] * a[2][2] +
               a[0][1] * a[1][2] * a[2][0] +
               a[0][2] * a[1][0] * a[2][1])

        neg = (a[0][2] * a[1][1] * a[2][0] +
               a[0][0] * a[1][2] * a[2][1] +
               a[0][1] * a[1][0] * a[2][2])

        return pos - neg

    def inversa(self):
        a = [linha[:] for linha in self.mat]
        n = len(a)

        if self.determinante() == 0:
            return None

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
        return Matriz(inverse)

    def transpose(self):
        if self.lin == 0 or self.col == 0:
            return Matriz([])

        transpose_matrix = []
        for j in range(self.col):
            nova_linha = []
            for i in range(self.lin):
                nova_linha.append(self.mat[i][j])
            transpose_matrix.append(nova_linha)

        return Matriz(transpose_matrix)