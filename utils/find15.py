from itertools import combinations, product


def find_target_combinations(numbers, target_values):
    for num_count in range(1, len(numbers) + 1):
        # Gere todas as combinações de 'num_count' números da lista
        num_combinations = combinations(numbers, num_count)
        for combination in num_combinations:
            # Gere todas as combinações de operadores (+, -) para os números
            operators = product(['+', '-'], repeat=num_count - 1)
            for operator_combination in operators:
                expression = ""
                result = 0
                for i, num in enumerate(combination):
                    expression += str(num)
                    if i < num_count - 1:
                        expression += operator_combination[i]
                try:
                    result = eval(expression)
                except ZeroDivisionError:
                    # Ignora divisões por zero
                    pass
                if result in target_values:
                    return expression, result
    return None, None

# Exemplo de uso:


def percorrer(lista_numeros):
    return_resultado = False
    valores_alvo = [14, 15, 16]
    expressao, resultado = find_target_combinations(lista_numeros, valores_alvo)
    while True:

        if expressao is None:
            print("Cai 1")
            break
        else:
            print(f"Expressão que atende ao valor alvo: {expressao} = {resultado}")
            valores_alvo.remove(resultado)
            expressao, resultado = find_target_combinations(lista_numeros, valores_alvo)
            return_resultado = True
    return return_resultado
