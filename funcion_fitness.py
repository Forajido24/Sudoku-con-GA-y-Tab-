import numpy as np

def contar_duplicados(arreglo):
    """
    *Cuenta cuantos elementos estan repetidos en el arreglo.
    *No cuenta las celdas vacias.
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
    Calcula errores del tablero:
    *duplicados en filas
    *duplicados en columnas
    *duplicados en subcuadros 3x3
    """
    tablero = np.array(tablero)
    errores = 0

    #Filas
    for fila in range(9):
        errores += contar_duplicados(tablero[fila, :])

    #Columnas
    for col in range(9):
        errores += contar_duplicados(tablero[:, col])

    #Subcuadros 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            sub = tablero[i:i+3, j:j+3].flatten()
            errores += contar_duplicados(sub)

    return errores
