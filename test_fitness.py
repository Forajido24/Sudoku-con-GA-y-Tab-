from sudoku import SudokuModel
from funcion_fitness import fitness
import numpy as np

# Sudoku de ejemplo (0 = vacío)
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Crear modelo
model = SudokuModel(board)

print("Generando individuo...")
individual = model.generate_individual()

# Imprimir el tablero generado
model.print_board(individual)

# Calcular fitness
f_val = fitness(np.array(individual))
print("\nFitness del tablero generado:", f_val)
