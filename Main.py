from Input import Input
from Matrix_Utils import Matriz
import random
import itertools
from Personalized_Exceptions import *

def caseAorCaseB(a, num_vars, artificial_vars, num_constraints):
    """
    Função auxiliar para adicionar as variáveis artificiais a matriz A antes da Fase 1.
    """
    try:
        print("Executando caseAorCaseB para adicionar variáveis artificiais, se necessário...")
        num_inequalities = 0
        inequality_line = 0
        line_size = len(a[0])
        aux_constraints = num_constraints
        for i in range(len(a)):
            if -1 in a[i][num_vars:]:
                num_inequalities += 1
                inequality_line = i
            if [0]*num_constraints == a[i][num_vars:]:
                num_inequalities += 1
                inequality_line = i
                aux_constraints += 1

        if num_inequalities < 2:
            line_size += 1
            if inequality_line == 0:
                for i in range(len(a)):
                    if -1 not in a[i][num_vars:] and 1 not in a[i][num_vars:]:
                        a[i].append(1)
                        artificial_vars.append(line_size)
                    else:
                        a[i].append(0)
                        artificial_vars.append(a[i][num_vars:].index(1) + num_vars + 1)
            else:
                for i in range(len(a)):
                    if -1 in a[i][num_vars:]:
                        a[i].append(1)
                        artificial_vars.append(line_size)
                    else:
                        a[i].append(0)
                        artificial_vars.append(a[i][num_vars:].index(1) + num_vars + 1)

        elif num_inequalities >= 2:
            if aux_constraints <= 3:
                aux = [[1 if i == j else 0 for j in range(num_inequalities)] for i in range(num_inequalities)]
                count_aux = 0
                for i in range(len(a)):
                    if -1 in a[i][num_vars:]:
                        line_size += 1
                        a[i].extend(aux[count_aux])
                        artificial_vars.append(line_size)
                        count_aux += 1
                    else:
                        a[i].extend([0] * num_inequalities)
                        artificial_vars.append(a[i][num_vars:].index(1) + num_vars + 1)
            else:
                aux = [[1 if i == j else 0 for j in range(aux_constraints)] for i in range(aux_constraints)]
                for i in range(len(a)):
                    line_size += 1
                    a[i].extend(aux[i])
                    artificial_vars.append(line_size)

        print("Variáveis artificiais adicionadas com sucesso.")
    except (IndexError, ValueError) as e:
        print(f"ERRO: Falha ao processar a matriz para adicionar variáveis artificiais: {e}")
        raise InvalidInputError(
            "As dimensões da matriz de restrições 'a' são inconsistentes ou os dados estão mal formatados.")

def generateBxNx(num_vars, num_constraints, a, c, b_xs=None, n_xs=None):
    """
    Gera as matrizes e vetores básicos (B) e não-básicos (N).
    """
    try:
        print("Gerando matrizes B, N e vetores de custo Cb, Cn...")
        if b_xs is None and n_xs is None:
            x_s = list(range(1, num_vars + num_constraints + 1))
            if num_constraints > len(x_s):
                raise InvalidInputError("O número de restrições excede o número total de variáveis.")
            b_xs = random.sample(x_s, num_constraints)
            b_xs.sort()
            n_xs = [x for x in x_s if x not in b_xs]
            n_xs.sort()

        b_x = [[a[i][index - 1] for index in b_xs] for i in range(len(a))]
        n_x = [[a[i][index - 1] for index in n_xs] for i in range(len(a))]

        cb = [c[i - 1] for i in b_xs]
        cn = [c[i - 1] for i in n_xs]

        print("Matrizes e vetores gerados com sucesso.")
        return b_xs, n_xs, b_x, n_x, cb, cn
    except IndexError as e:
        print(f"ERRO: Índice fora do alcance ao gerar matrizes B e N: {e}")
        raise InvalidInputError("Inconsistência entre os índices das variáveis e as dimensões das matrizes 'a' ou 'c'.")


def basic_solution_calc(bx, b):
    """
    Calcula a solução básica atual.
    """
    try:
        print("Calculando a solução básica (Xb)...")
        xb_approximation = bx.inversa().__mul__(b.transpose())
        xn_approximation = [0] * len(b.mat)
        print("Solução básica calculada.")
        return xb_approximation, xn_approximation
    except ValueError as e:
        print(f"ERRO: O problema pode ser inviável devido a uma base singular. {e}")
        raise InfeasibleProblemError("A matriz básica B é singular, o que indica restrições linearmente dependentes.")


def relative_cost(bx, nx, cb, cn):
    """
    Calcula os custos relativos.
    """
    try:
        print("Calculando os custos relativos...")
        bx_inverse = bx.inversa()
        lambda_vector = cb.__mul__(bx_inverse)
        print(f"Multiplicador Simplex (λ): {lambda_vector.mat}")

        nx_t = nx.transpose()
        ax = [Matriz(i).transpose() for i in nx_t.mat]
        current_relative_costs = [cn.mat[0][i] - lambda_vector.__mul__(ax[i]).mat[0][0] for i in range(len(cn.mat[0]))]

        print(f"Custos Relativos: {current_relative_costs}")
        return current_relative_costs
    except (ValueError, IndexError) as e:
        print(f"ERRO no cálculo do custo relativo: {e}")
        raise InvalidInputError("Erro de dimensão durante o cálculo do custo relativo. Verifique as matrizes B e N.")


def simplex_direction_calc(nx, bx, index_min):
    """
    Calcula a direção Simplex (y).
    """
    try:
        print("Calculando a direção Simplex (y)...")
        ax = nx.transpose().mat[index_min]
        y = bx.inversa().__mul__(Matriz(ax).transpose())
        print(f"Vetor y: {y.mat}")
        return y
    except (ValueError, IndexError) as e:
        print(f"ERRO ao calcular a direção simplex: {e}")
        raise InvalidInputError("Erro de dimensão ou índice inválido no cálculo da direção y.")

def det_step_var_to_leave_the_base(y, xb, xn, entering_var, xb_approximation):
    """
    Determina a variável que sai da base (critério da razão).
    """
    try:
        print("Determinando a variável que sairá da base...")
        epsilon_candidates = []
        indices_for_epsilon_candidates = []
        for i in range(len(xb)):
            if y.mat[i][0] > 0:
                epsilon_candidates.append(xb_approximation.mat[i][0] / y.mat[i][0])
                indices_for_epsilon_candidates.append(i)

        if not epsilon_candidates:
            raise UnboundedProblemError("O problema é ilimitado, pois não há variável para sair da base.")

        min_epsilon = min(epsilon_candidates)
        leaving_var_local_index = indices_for_epsilon_candidates[epsilon_candidates.index(min_epsilon)]

        print(f"Variável {xn[entering_var]} entra na base, variável {xb[leaving_var_local_index]} sai da base.")

        temp_var_for_swap = xn[entering_var]
        xn[entering_var] = xb[leaving_var_local_index]
        xb[leaving_var_local_index] = temp_var_for_swap

        return xb, xn

    except ValueError as e:
        print(f"ERRO: Problema ilimitado. {e}")
        raise UnboundedProblemError(
            "O problema é ilimitado (solução ótima infinita), pois todos os elementos da direção y são não-positivos.")
    except IndexError as e:
        print(f"ERRO: Índice fora do alcance na troca de variáveis da base: {e}")
        raise InvalidInputError("Erro de lógica ou dados ao tentar trocar variáveis entre a base e a não-base.")


def artificial_vars_base(artificial_vars, xb):
    """
    Verifica se ainda existem variáveis artificiais na base.
    """
    for var in artificial_vars:
        if var in xb:
            return False
    return True

def fase1(a, b, c, num_vars, num_constraints, artificial_vars):
    """
    Executa a Fase 1 do método Simplex para encontrar uma solução básica viável.
    """
    print("\n--- Início da Fase 1 ---")
    try:
        objective_coeffs = [0] * (num_vars + num_constraints)
        objective_coeffs.extend([1] * (len(a[0]) - len(objective_coeffs)))

        xb = artificial_vars.copy()
        xn = [i + 1 for i in range(num_vars + num_constraints)]

        xb, xn, bx, nx, cb, cn = generateBxNx(len(objective_coeffs), num_constraints, a, objective_coeffs, b_xs=xb, n_xs=xn)

        iteration = 1
        while True:
            print(f"\n--- Fase 1: Iteração {iteration} ---")
            print(f"Base (índices): {xb}")
            print(f"Não-Base (índices): {xn}")

            bx_mat = Matriz(bx)
            nx_mat = Matriz(nx)
            cb_mat = Matriz(cb)
            cn_mat = Matriz(cn)

            xb_approximation, _ = basic_solution_calc(bx_mat, b)
            print(f"Solução básica (Xb): {[row[0] for row in xb_approximation.mat]}")

            current_relative_costs = relative_cost(bx_mat, nx_mat, cb_mat, cn_mat)
            if not current_relative_costs:
                raise InvalidInputError("O cálculo do custo relativo retornou uma lista vazia.")

            min_relative_cost = min(current_relative_costs)

            if min_relative_cost >= 0:
                if artificial_vars_base(artificial_vars, xb):
                    raise InfeasibleProblemError("Problema infactível.")
                else:
                    print("Fim da Fase 1: Solução básica viável encontrada.")
                    return xb, xn

            index_min = current_relative_costs.index(min_relative_cost)

            y = simplex_direction_calc(nx_mat, bx_mat, index_min)

            xb, xn = det_step_var_to_leave_the_base(y, xb, xn, index_min, xb_approximation)

            xb, xn, bx, nx, cb, cn = generateBxNx(len(objective_coeffs), num_constraints, a, objective_coeffs, xb, xn)
            iteration += 1

    except (InfeasibleProblemError, UnboundedProblemError, InvalidInputError) as e:
        print(f"ERRO na Fase 1: {e}")
        raise

def fase2(a, b, c, num_vars, num_constraints, xb_initial=None, xn_initial=None):
    """
    Executa a Fase 2 do método Simplex para encontrar a solução ótima.
    """
    print("\n--- Início da Fase 2 ---")
    a_fase2 = [row[:num_vars + num_constraints] for row in a]
    c_fase2 = c[:num_vars + num_constraints]

    if xb_initial is not None and xn_initial is not None:
        print("Fase 2 iniciada com base fornecida.")
        try:
            current_xb_indices, current_xn_indices, bx, nx, cb, cn = generateBxNx(
                num_vars, num_constraints, a_fase2, c_fase2, b_xs=xb_initial, n_xs=xn_initial
            )

            iteration = 1
            while True:
                print(f"\n--- Fase 2 (Base Fixa {current_xb_indices}): Iteração {iteration} ---")

                bx_mat = Matriz(bx)
                nx_mat = Matriz(nx)
                cb_mat = Matriz(cb)
                cn_mat = Matriz(cn)
                xb_approximation, _ = basic_solution_calc(bx_mat, b)
                print(f"Solução básica (Xb): {[round(row[0], 6) for row in xb_approximation.mat]}")

                current_relative_costs = relative_cost(bx_mat, nx_mat, cb_mat, cn_mat)
                if not current_relative_costs:
                    raise InvalidInputError("Custo relativo retornou uma lista vazia na Fase 2.")

                min_relative_cost = min(current_relative_costs)

                if min_relative_cost >= 0:
                    z = sum(xb_approximation.mat[i][0] * cb[i] for i in range(len(cb)))
                    if z == 0:
                        raise InvalidInputError("Problema insolusionável")
                    print("\n--- Solução Ótima Encontrada (Base Fixa) ---")
                    return z, xb_approximation.mat, current_xb_indices

                index_min_entering = current_relative_costs.index(min_relative_cost)

                y = simplex_direction_calc(nx_mat, bx_mat, index_min_entering)

                new_xb_indices, new_xn_indices = det_step_var_to_leave_the_base(
                    y, current_xb_indices, current_xn_indices, index_min_entering, xb_approximation
                )

                current_xb_indices, current_xn_indices, bx, nx, cb, cn = generateBxNx(
                    num_vars, num_constraints, a_fase2, c_fase2, b_xs=new_xb_indices, n_xs=new_xn_indices
                )
                iteration += 1

        except (InfeasibleProblemError, UnboundedProblemError, InvalidInputError) as e:
            print(f"ERRO na Fase 2 (com base inicial fornecida {xb_initial}): {e}")
            raise

    else:
        print("Fase 2 iniciada sem base. Tentando gerar todas as bases possíveis...")
        all_vars_indices = list(range(1, num_vars + num_constraints + 1))

        if num_constraints > len(all_vars_indices):
            raise InvalidInputError("O número de restrições excede o número total de variáveis disponíveis.")
        if num_constraints == 0:
            print("AVISO: Número de restrições é 0. Verifique a formulação do problema.")
            if any(cost < 0 for cost in c_fase2):
                raise UnboundedProblemError(
                    "Problema ilimitado (0 restrições, custos favoráveis à otimização infinita).")
            print("\n--- Solução Ótima Encontrada (0 restrições, Z=0) ---")
            return 0.0

        candidate_base_indices_combinations = itertools.combinations(all_vars_indices, num_constraints)

        tested_bases_count = 0
        for b_xs_combination_tuple in candidate_base_indices_combinations:
            permutations_of_current_combination = itertools.permutations(list(b_xs_combination_tuple))

            for permuted_b_xs_list in permutations_of_current_combination:
                permuted_b_xs = list(permuted_b_xs_list)
                n_xs = sorted([x for x in all_vars_indices if x not in permuted_b_xs])
                tested_bases_count += 1

                print(f"\n--- Tentando Fase 2 com Base candidata {tested_bases_count}: {permuted_b_xs} ---")

                try:
                    current_xb_indices, current_xn_indices, bx, nx, cb, cn = generateBxNx(
                        num_vars, num_constraints, a_fase2, c_fase2, b_xs=permuted_b_xs, n_xs=n_xs
                    )

                    iteration = 1
                    temp_xb_indices = list(current_xb_indices)
                    temp_xn_indices = list(current_xn_indices)
                    temp_bx, temp_nx, temp_cb, temp_cn = bx, nx, cb, cn

                    while True:
                        print(f"\n--- Fase 2 (Base {temp_xb_indices}): Iteração {iteration} ---")

                        bx_mat_loop = Matriz(temp_bx)
                        nx_mat_loop = Matriz(temp_nx)
                        cb_mat_loop = Matriz(temp_cb)
                        cn_mat_loop = Matriz(temp_cn)

                        xb_approximation, _ = basic_solution_calc(bx_mat_loop, b)  # 'b' já é Matriz
                        print(f"Solução básica (Xb): {[round(row[0], 6) for row in xb_approximation.mat]}")

                        if any(val[0] < -1e-9 for val in xb_approximation.mat):
                            print(
                                f"AVISO: Base {temp_xb_indices} resultou em solução básica inviável (Xb < 0). Tentando próxima base.")
                            raise InfeasibleProblemError(
                                "Solução básica Xb < 0.")

                        current_relative_costs = relative_cost(bx_mat_loop, nx_mat_loop, cb_mat_loop, cn_mat_loop)
                        if not current_relative_costs:
                            print(
                                f"ERRO: Custo relativo retornou lista vazia para base {temp_xb_indices}. Tentando próxima base.")
                            raise InvalidInputError("Custo relativo retornou uma lista vazia na Fase 2.")

                        min_relative_cost = min(current_relative_costs)

                        if min_relative_cost >= -1e-9:
                            z_loop = sum(xb_approximation.mat[i][0] * temp_cb[i] for i in range(len(temp_cb)))
                            if z_loop == 0:
                                raise InvalidInputError("Problema insolusionável")
                            print(f"\n--- Solução Ótima Encontrada com Base {temp_xb_indices} ---")
                            return z_loop, xb_approximation.mat, current_xb_indices

                        index_min_entering_loop = current_relative_costs.index(min_relative_cost)

                        y_loop = simplex_direction_calc(nx_mat_loop, bx_mat_loop, index_min_entering_loop)

                        temp_xb_indices, temp_xn_indices = det_step_var_to_leave_the_base(
                            y_loop, temp_xb_indices, temp_xn_indices, index_min_entering_loop, xb_approximation
                        )

                        temp_xb_indices, temp_xn_indices, temp_bx, temp_nx, temp_cb, temp_cn = generateBxNx(
                            num_vars, num_constraints, a_fase2, c_fase2, b_xs=temp_xb_indices, n_xs=temp_xn_indices
                        )
                        iteration += 1

                except InfeasibleProblemError as e:
                    print(
                        f"AVISO: Base {permuted_b_xs} não levou a uma solução viável (ex: singular, Xb<0). {e}. Tentando próxima base...")
                except UnboundedProblemError as e:
                    print(f"ERRO: Problema Ilimitado encontrado com base {permuted_b_xs}. {e}")
                    raise
                except InvalidInputError as e:
                    print(f"ERRO: Entrada inválida com base {permuted_b_xs}. {e}. Tentando próxima base...")
        print(
            f"ERRO: Nenhuma base funcional (invertível e levando à otimalidade ou ilimitabilidade) encontrada após testar {tested_bases_count} candidatas.")
        raise InfeasibleProblemError(
            "Não foi possível encontrar uma solução ótima ou determinar ilimitabilidade após testar todas as combinações de base.")

def main():
    try:
        input_obj = Input("Inputs/5_7-q.txt")
        input_obj.read()
        c, a, b = input_obj.getInputs()

        print("--- Entrada Inicial ---")
        print(f"Vetor Custo (c): {c}")
        print(f"Matriz de Restrições (a): {a}")
        print(f"Vetor de Termos Independentes (b): {b}")

        num_vars, num_constraints = input_obj.getNumVars()

        xb_final, xn_final = None, None

        if input_obj.necessity_fase1:
            artificial_vars = []
            caseAorCaseB(a, num_vars, artificial_vars, num_constraints)
            print(f"\nMatriz 'a' após adicionar vars artificiais: {a}")

            b_mat = Matriz(b)
            xb_final, xn_final = fase1(a, b_mat, c, num_vars, num_constraints, artificial_vars)
            xn_final = [i for i in xn_final if i not in artificial_vars]

        b_mat = Matriz(b)
        z, xb_vals, xb_indices = fase2(a, b_mat, c, num_vars, num_constraints, xb_final, xn_final)

        coef_result = 1
        if input_obj.opt == "max":
            coef_result = -1
        print("\n======================================")
        print(f"VALOR ÓTIMO (Z): {coef_result*round(z, 2)}")
        print("======================================")
        print("\n======================================")
        vars_indices = [i for i in range(1, num_vars+1)]
        for i in range(len(xb_indices)):
            if xb_indices[i] in vars_indices:
                print(f"X{xb_indices[i]}: {coef_result*xb_vals[i][0]}")

        print("======================================")
    except FileNotFoundError:
        print("ERRO CRÍTICO: O arquivo de entrada não foi encontrado.")
    except (InfeasibleProblemError, UnboundedProblemError, InvalidInputError) as e:
        print("\n======================================")
        print(f"FALHA NA EXECUÇÃO: {e}")
        print("======================================")
    except Exception as e:
        print("\n======================================")
        print(f"UM ERRO INESPERADO OCORREU: {e}")
        print("======================================")


if __name__ == '__main__':
    main()