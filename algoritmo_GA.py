import numpy as np
import random
from sudoku import SudokuModelo
from funcion_fitness import evaluar_fitness

class AlgoritmoGeneticoSudoku:
    def __init__(self, tablero_base, tam_poblacion=100, generaciones=200, tasa_mutacion=0.1, elitismo=True):
        """
        tablero_base: puede ser un SudokuModelo o una matriz/lista 9x9.
        """
        # Aceptar tanto SudokuModelo como tablero (lista/np.array)
        if isinstance(tablero_base, SudokuModelo):
            self.modelo = tablero_base
        else:
            # validación ligera
            self.modelo = SudokuModelo(tablero_base)

        self.tam_poblacion = tam_poblacion
        self.generaciones = generaciones
        self.tasa_mutacion = tasa_mutacion
        self.elitismo = elitismo

    # ----------------------------
    # Población inicial (usa generar_individuo del modelo)
    # ----------------------------
    def generar_poblacion(self):
        poblacion = []
        for _ in range(self.tam_poblacion):
            individuo = self.modelo.generar_individuo()
            poblacion.append(individuo)
        return poblacion

    # ----------------------------
    # Selección por torneo (k=3)
    # ----------------------------
    def seleccion_torneo(self, poblacion, k=3):
        candidatos = random.sample(poblacion, k)
        valores = [evaluar_fitness(ind) for ind in candidatos]
        mejor_idx = int(np.argmin(valores))
        return candidatos[mejor_idx]

    # ----------------------------
    # Cruce por filas
    # ----------------------------
    def cruce(self, padre1, padre2):
        hijo = np.copy(padre1)
        for fila in range(9):
            if random.random() < 0.5:
                hijo[fila] = padre2[fila]
        return hijo

    # ----------------------------
    # Mutación: intercambio dentro de la misma fila (o subcuadro)
    # ----------------------------
    def mutacion(self, individuo):
        ind = np.copy(individuo)

        # Aquí usamos el enfoque por subcuadros (mantener subcuadros "completos")
        for fila_bloque in range(0, 9, 3):
            for col_bloque in range(0, 9, 3):
                if random.random() < self.tasa_mutacion:
                    posiciones_editables = []
                    for f in range(fila_bloque, fila_bloque + 3):
                        for c in range(col_bloque, col_bloque + 3):
                            if not self.modelo.mascara_fijas[f, c]:
                                posiciones_editables.append((f, c))

                    if len(posiciones_editables) >= 2:
                        a, b = random.sample(posiciones_editables, 2)
                        ind[a], ind[b] = ind[b], ind[a]

        return ind

    # ----------------------------
    # Ejecutar GA
    # ----------------------------
    def ejecutar(self):
        poblacion = self.generar_poblacion()
        historial = []

        mejor_individuo = None
        mejor_fitness = float("inf")

        for gen in range(self.generaciones):
            fitness_vals = [evaluar_fitness(ind) for ind in poblacion]
            idx_mejor = int(np.argmin(fitness_vals))
            mejor_actual = poblacion[idx_mejor]
            mejor_val = fitness_vals[idx_mejor]

            historial.append(mejor_val)

            print(f"Generación {gen} - Mejor fitness: {mejor_val}")

            if mejor_val < mejor_fitness:
                mejor_fitness = mejor_val
                mejor_individuo = mejor_actual.copy()

            if mejor_val == 0:
                print("¡Sudoku resuelto!")
                return mejor_individuo, historial

            nueva_poblacion = []

            if self.elitismo:
                nueva_poblacion.append(mejor_actual)

            while len(nueva_poblacion) < self.tam_poblacion:
                p1 = self.seleccion_torneo(poblacion)
                p2 = self.seleccion_torneo(poblacion)

                hijo = self.cruce(p1, p2)
                hijo = self.mutacion(hijo)
                nueva_poblacion.append(hijo)

            poblacion = nueva_poblacion

        print("No se encontró solución perfecta. Devolviendo mejor individuo encontrado.")
        return mejor_individuo, historial
