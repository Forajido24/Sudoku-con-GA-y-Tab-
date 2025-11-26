# algoritmo_tabu.py
import numpy as np
from collections import deque
import random

class TabuSudoku:
    def __init__(self, modelo_sudoku, max_iter=500, tabu_tam=50):
        self.model = modelo_sudoku
        self.max_iter = max_iter
        self.tabu = deque(maxlen=tabu_tam)

    def fitness(self, tablero):
        """Número de conflictos en filas, columnas y subcuadros."""
        conflictos = 0

        # Filas
        for fila in tablero:
            valores, counts = np.unique(fila[fila > 0], return_counts=True)
            conflictos += np.sum(counts[counts > 1] - 1)

        # Columnas
        for col in tablero.T:
            valores, counts = np.unique(col[col > 0], return_counts=True)
            conflictos += np.sum(counts[counts > 1] - 1)

        # Subcuadros
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                sub = tablero[r:r+3, c:c+3].flatten()
                valores, counts = np.unique(sub[sub > 0], return_counts=True)
                conflictos += np.sum(counts[counts > 1] - 1)

        return conflictos

    def generar_vecino(self, tablero):
        """Hace un swap en un subcuadro 3×3 evitando celdas fijas."""
        nueva = tablero.copy()

        # Elegir subcuadro
        sr = random.choice([0, 3, 6])
        sc = random.choice([0, 3, 6])

        # Celdas no fijas en este bloque
        libres = [(r, c) for r in range(sr, sr+3)
                        for c in range(sc, sc+3)
                        if not self.model.fixed_mask[r, c]]

        if len(libres) < 2:
            return nueva

        # Swap
        a, b = random.sample(libres, 2)
        nueva[a], nueva[b] = nueva[b], nueva[a]

        return nueva

    def ejecutar(self):
        tablero = self.model.tablero.copy()

        mejor = tablero.copy()
        mejor_fit = self.fitness(tablero)

        for _ in range(self.max_iter):

            vecino = self.generar_vecino(tablero)
            mov_hash = vecino.tobytes()

            if mov_hash in self.tabu:
                continue

            fit = self.fitness(vecino)

            # Si es mejor → aceptar
            if fit < mejor_fit:
                mejor = vecino.copy()
                mejor_fit = fit

            # Move
            tablero = vecino
            self.tabu.append(mov_hash)

            # Sudoku resuelto
            if mejor_fit == 0:
                break

        return mejor, mejor_fit
