class Matriz():
    def __init__(self, mat_input):
        if isinstance(mat_input, list) and mat_input and \
                all(isinstance(x, (int, float)) for x in mat_input) and \
                not any(isinstance(x, list) for x in
                        mat_input):
            mat_data = [list(mat_input)]
        elif isinstance(mat_input, list):
            mat_data = [list(row) if isinstance(row, list) else row for row in mat_input]
        else:
            raise TypeError("A entrada da matriz deve ser uma lista (para um vetor linha) ou uma lista de listas.")

        if not isinstance(mat_data, list):
            raise TypeError("A estrutura interna da matriz deve ser uma lista de listas.")

        self.mat = mat_data
        self.lin = len(self.mat)

        if self.lin == 0:
            self.col = 0
            return

        primeira_linha_tipo_lista = isinstance(self.mat[0], list)
        if not primeira_linha_tipo_lista:
            raise TypeError("A matriz deve ser composta por uma lista de listas (linhas).")

        self.col = len(self.mat[0])
        for i, linha in enumerate(self.mat):
            if not isinstance(linha, list):
                raise TypeError(f"Elemento na linha {i} não é uma lista. A matriz deve ser uma lista de listas.")
            if len(linha) != self.col:
                raise ValueError(
                    f"Todas as linhas devem ter o mesmo número de colunas. Linha 0 tem {self.col}, linha {i} tem {len(linha)}.")
            if not all(isinstance(val, (int, float)) for val in linha):
                raise ValueError(f"Todos os elementos da matriz devem ser números (int ou float). Erro na linha {i}.")

    def getLinha(self, n):
        if not isinstance(n, int):
            raise TypeError("O índice da linha deve ser um inteiro.")
        if not (0 <= n < self.lin):
            raise IndexError(f"Índice da linha {n} fora dos limites (0 a {self.lin - 1}).")
        return list(self.mat[n])

    def getColuna(self, n):
        if not isinstance(n, int):
            raise TypeError("O índice da coluna deve ser um inteiro.")
        if self.lin == 0 and n == 0:
            if self.col == 0:
                raise IndexError(f"Índice da coluna {n} fora dos limites para uma matriz com {self.col} colunas.")
        if not (0 <= n < self.col):
            raise IndexError(f"Índice da coluna {n} fora dos limites (0 a {self.col - 1}).")
        if self.lin == 0:
            return []
        return [self.mat[i][n] for i in range(self.lin)]

    def __mul__(self, mat2):
        if not isinstance(mat2, Matriz):
            raise TypeError("A multiplicação só pode ser feita com outra instância da classe Matriz.")
        if self.col != mat2.lin:
            raise ValueError(
                f"Número de colunas da primeira matriz ({self.col}) "
                f"deve ser igual ao número de linhas da segunda matriz ({mat2.lin})."
            )
        if self.lin == 0 or self.col == 0 or mat2.lin == 0 or mat2.col == 0:
            if self.col == 0 and mat2.lin == 0:
                return Matriz([[] for _ in range(self.lin)]) if self.lin > 0 and mat2.col == 0 else Matriz([])

        matRes = []
        for i in range(self.lin):
            matRes.append([])
            for j in range(mat2.col):
                linha_da_mat1 = self.getLinha(i)
                coluna_da_mat2 = mat2.getColuna(j)

                listMult = [x * y for x, y in zip(linha_da_mat1, coluna_da_mat2)]
                matRes[i].append(sum(listMult))

        if not matRes and self.lin > 0 and mat2.col == 0:
            return Matriz([[] for _ in range(self.lin)])
        if not matRes and self.lin == 0 and mat2.col > 0:
            return Matriz([])

        return Matriz(matRes)

    def determinante(self):
        if self.lin != self.col:
            raise ValueError("Determinante só pode ser calculado para matrizes quadradas.")

        n = self.lin
        if n == 0:

            return 1

        matriz_copia = [list(linha) for linha in self.mat]  # Trabalhar com uma cópia

        if n == 1:
            return matriz_copia[0][0]

        if n == 2:
            return matriz_copia[0][0] * matriz_copia[1][1] - matriz_copia[0][1] * matriz_copia[1][0]

        if n == 3:
            return self._sarrus()

        det = 0
        for col_criterio in range(n):
            submatriz_data = []
            for i in range(1, n):
                linha_submatriz = []
                for j in range(n):
                    if j != col_criterio:
                        linha_submatriz.append(matriz_copia[i][j])
                submatriz_data.append(linha_submatriz)

            sinal = (-1) ** col_criterio
            sub_matriz_obj = Matriz(submatriz_data)
            cofator = sinal * sub_matriz_obj.determinante()
            det += matriz_copia[0][col_criterio] * cofator
        return det

    def _sarrus(self):
        if self.lin != 3 or self.col != 3:
            raise ValueError("A regra de Sarrus é aplicável apenas a matrizes 3x3.")

        a = self.mat
        pos = (a[0][0] * a[1][1] * a[2][2] +
               a[0][1] * a[1][2] * a[2][0] +
               a[0][2] * a[1][0] * a[2][1])
        neg = (a[0][2] * a[1][1] * a[2][0] +
               a[0][0] * a[1][2] * a[2][1] +
               a[0][1] * a[1][0] * a[2][2])
        return pos - neg

    def inversa(self):
        if self.lin != self.col:
            raise ValueError("A matriz deve ser quadrada para calcular a inversa.")
        if self.lin == 0:
            raise ValueError("Não é possível calcular a inversa de uma matriz 0x0.")

        det = self.determinante()
        epsilon = 1e-9
        if abs(det) < epsilon:
            raise ValueError("A matriz é singular (determinante próximo de zero) e não pode ser invertida.")

        n = self.lin
        matriz_copia = [list(linha) for linha in self.mat]

        identidade = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

        aumentada = [matriz_copia[i] + identidade[i] for i in range(n)]

        for col_pivot in range(n):

            pivot_val = aumentada[col_pivot][col_pivot]

            if abs(pivot_val) < epsilon:
                linha_troca = -1
                for r_busca in range(col_pivot + 1, n):
                    if abs(aumentada[r_busca][col_pivot]) > epsilon:
                        linha_troca = r_busca
                        break
                if linha_troca != -1:
                    aumentada[col_pivot], aumentada[linha_troca] = aumentada[linha_troca], aumentada[col_pivot]
                    pivot_val = aumentada[col_pivot][col_pivot]
                else:
                    raise ValueError(
                        "Matriz singular encontrada durante a eliminação de Gauss-Jordan; não pode ser invertida.")

            for j in range(col_pivot, 2 * n):
                aumentada[col_pivot][j] /= pivot_val

            for i in range(n):
                if i != col_pivot:
                    fator = aumentada[i][col_pivot]
                    for j in range(col_pivot, 2 * n):
                        aumentada[i][j] -= fator * aumentada[col_pivot][j]

        inversa_data = [linha[n:] for linha in aumentada]
        return Matriz(inversa_data)

    def transpose(self):
        if self.lin == 0 and self.col == 0:
            return Matriz([])
        if self.lin > 0 and self.col == 0:
            return Matriz([])

        matriz_transposta_data = []
        for j in range(self.col):
            nova_linha = []
            for i in range(self.lin):
                nova_linha.append(self.mat[i][j])
            matriz_transposta_data.append(nova_linha)

        return Matriz(matriz_transposta_data)

    def __str__(self):
        if not self.mat:
            return "[ Matriz Vazia ]"
        return "\n".join(["[" + ", ".join(map(str, linha)) + "]" for linha in self.mat])

    def __repr__(self):
        return f"Matriz({self.mat})"