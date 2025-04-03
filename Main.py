from Input import Input
from Matrix_Utils import matrix_product, sarrus, determinant, inverse_matrix

input = Input("Inputs/inputs1.txt")

input.read()

c, a, b = input.getInputs()

print(c)
print(a)
print(b)

# matriz_a = [[1, 2, 3], [0, 1, 0], [1, 0, 2]]
# print(inverse_matrix(matriz_a))