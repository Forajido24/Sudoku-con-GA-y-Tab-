import numpy as np

def contar_duplicados(arreglo):
    """
    Cuenta cuántos elementos están repetidos en 'arreglo' (array 1D).
    No cuenta ceros (celdas vacías).
    Ejemplo: [1,2,2,3,3,3] -> devuelve 3 (1 duplicado para 2, 2 duplicados para 3)
    """
    valores, conteos = np.unique(arreglo, return_counts=True)
    duplicados = 0
    for v, c in zip(valores, conteos):
        if v == 0:
            continue
        if c > 1:
            duplicados += (c - 1)
    return duplicados

def evaluar_fitness(tablero):
    """
    Calcula errores (fitness) de un tablero 9x9:
    - duplicados en filas
    - duplicados en columnas
    - duplicados en subcuadros 3x3
    Fitness más bajo = mejor.
    """
    tablero = np.array(tablero)
    errores = 0

    # Filas
    for fila in range(9):
        errores += contar_duplicados(tablero[fila, :])

    # Columnas
    for col in range(9):
        errores += contar_duplicados(tablero[:, col])

    # Subcuadros 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            sub = tablero[i:i+3, j:j+3].flatten()
            errores += contar_duplicados(sub)

    return errores
