import numpy as np

def contar_duplicados(arreglo):
    """
    Cuenta cuantos elementos estan repetidos.
    Ignora ceros.
    """
    vals, counts = np.unique(arreglo, return_counts=True)
    return sum((c - 1) for v, c in zip(vals, counts) if v != 0 and c > 1)


def evaluar_fitness(tablero):
    """
    Fitness optimizado:
    * duplicados en filas
    * duplicados en columnas
    
    (No evalúa subcuadros porque tu GA y TABU ya garantizan validez en 3×3)
    """
    tablero = np.array(tablero)
    errores = 0

    # Filas
    for f in range(9):
        errores += contar_duplicados(tablero[f])

    # Columnas
    for c in range(9):
        errores += contar_duplicados(tablero[:, c])

    return errores
