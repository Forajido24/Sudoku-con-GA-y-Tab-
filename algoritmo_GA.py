import numpy as np
import random
from funcion_fitness import evaluar_fitness
from sudoku import SudokuModelo


class AlgoritmoGeneticoSudoku:

    def __init__(self, tablero_base, tam_poblacion=150, generaciones=200,
                 tasa_mutacion=0.2, elitismo=True):

        if isinstance(tablero_base, SudokuModelo):
            self.modelo = tablero_base
        else:
            self.modelo = SudokuModelo(tablero_base)

        self.tam_poblacion = tam_poblacion
        self.generaciones = generaciones
        self.tasa_mutacion = tasa_mutacion
        self.elitismo = elitismo

    # ---------------------------------------------------------
    # Generar la POBLACIÓN INICIAL
    # ---------------------------------------------------------
    def generar_poblacion(self):
        return [self.modelo.generar_individuo() for _ in range(self.tam_poblacion)]

    # ---------------------------------------------------------
    # Selección por TORNEO
    # ---------------------------------------------------------
    def seleccion_torneo(self, poblacion, k=5):
        candidatos = random.sample(poblacion, k)
        fitness_vals = [evaluar_fitness(ind) for ind in candidatos]
        return candidatos[int(np.argmin(fitness_vals))]

    # ---------------------------------------------------------
    # CRUCE por BLOQUES 3×3 (respeta celdas fijas)
    # ---------------------------------------------------------
    def cruce(self, padre1, padre2):
        hijo = padre1.copy()

        for fb in range(0, 9, 3):
            for cb in range(0, 9, 3):

                if random.random() < 0.5:
                    bloque2 = padre2[fb:fb+3, cb:cb+3]
                    bloque_fijo = self.modelo.mascara_fijas[fb:fb+3, cb:cb+3]

                    for i in range(3):
                        for j in range(3):
                            if not bloque_fijo[i, j]:
                                hijo[fb+i, cb+j] = bloque2[i, j]

        return hijo

    # ---------------------------------------------------------
    # MUTACIÓN por BLOQUES (swap dentro del subcuadro)
    # ---------------------------------------------------------
    def mutacion(self, individuo):
        hijo = individuo.copy()

        for fb in range(0, 9, 3):
            for cb in range(0, 9, 3):

                if random.random() < self.tasa_mutacion:

                    libres = []
                    for i in range(3):
                        for j in range(3):
                            if not self.modelo.mascara_fijas[fb+i, cb+j]:
                                libres.append((fb+i, cb+j))

                    if len(libres) >= 2:
                        a, b = random.sample(libres, 2)
                        hijo[a], hijo[b] = hijo[b], hijo[a]

        return hijo

    # ---------------------------------------------------------
    # EJECUTAR GA
    # ---------------------------------------------------------
    def ejecutar(self):
        poblacion = self.generar_poblacion()
        historial = []

        mejor_individuo = None
        mejor_fitness = float("inf")

        for gen in range(self.generaciones):
            fitness_vals = [evaluar_fitness(ind) for ind in poblacion]
            idx_mejor = int(np.argmin(fitness_vals))

            gen_mejor = poblacion[idx_mejor]
            gen_fit = fitness_vals[idx_mejor]
            historial.append(gen_fit)

            print(f"Gen {gen} - Fitness: {gen_fit}")

            # Actualizar mejor global
            if gen_fit < mejor_fitness:
                mejor_fitness = gen_fit
                mejor_individuo = gen_mejor.copy()

            if mejor_fitness == 0:
                print("✔ GA resolvió el Sudoku!")
                return mejor_individuo, historial

            # Nueva población
            nueva_pob = []

            # ELITISMO
            if self.elitismo:
                nueva_pob.append(gen_mejor.copy())

            # Rellenar el resto
            while len(nueva_pob) < self.tam_poblacion:
                p1 = self.seleccion_torneo(poblacion)
                p2 = self.seleccion_torneo(poblacion)

                hijo = self.cruce(p1, p2)
                hijo = self.mutacion(hijo)
                nueva_pob.append(hijo)

            poblacion = nueva_pob

        print("⚠ No se logró solución perfecta. Retornando mejor aproximación.")
        return mejor_individuo, historial
