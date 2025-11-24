import numpy as np

def count_duplicates(arr):
    """
    Cuenta cuántas repeticiones hay en un arreglo.
    Ejemplo:
        [1, 2, 2, 3, 3, 3] → 3 errores
    """
    vals, counts = np.unique(arr, return_counts=True)
    
    # No contamos ceros porque no deben penalizar
    duplicates = sum(c - 1 for v, c in zip(vals, counts) if v != 0 and c > 1)
    return duplicates


def fitness(board):
    """
    Calcula el fitness total de un Sudoku:
    - Errores por filas
    - Errores por columnas
    - Fitness bajo = mejor
    """
    total_errors = 0

    # Errores por filas
    for row in range(9):
        total_errors += count_duplicates(board[row])

    # Errores por columnas
    for col in range(9):
        total_errors += count_duplicates(board[:, col])

    return total_errors
