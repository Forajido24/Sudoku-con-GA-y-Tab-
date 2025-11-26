import numpy as np
import random
from sudoku import SudokuModelo
from funcion_fitness import evaluar_fitness

class AlgoritmoGeneticoSudoku:

    #Inicializamos el algoritmo genético con parametros
    def __init__(self, tablero_base, tam_poblacion=100, generaciones=200, tasa_mutacion=0.1, elitismo=True):
        
        if isinstance(tablero_base, SudokuModelo):
            self.modelo = tablero_base
        else:

            self.modelo = SudokuModelo(tablero_base)

        self.tam_poblacion = tam_poblacion
        self.generaciones = generaciones
        self.tasa_mutacion = tasa_mutacion
        self.elitismo = elitismo

    #Generamos la poblacion inicial
    def generar_poblacion(self):
        poblacion = []
        for _ in range(self.tam_poblacion):
            individuo = self.modelo.generar_individuo()
            poblacion.append(individuo)
        return poblacion

    #Seleccion por torneo, escogemos el mejor entre k individuos
    def seleccion_torneo(self, poblacion, k=3):
        candidatos = random.sample(poblacion, k)
        valores = [evaluar_fitness(ind) for ind in candidatos]
        mejor_idx = int(np.argmin(valores))
        return candidatos[mejor_idx]
    
    #Cruce entre dos padres para generar un hijo
    def cruce(self, padre1, padre2):
        hijo = np.copy(padre1)
        for fila in range(9):
            if random.random() < 0.5:
                hijo[fila] = padre2[fila]
        return hijo

    #Mutacion del individuo
    def mutacion(self, individuo):
        ind = np.copy(individuo)
        #Recorremos los bloques 3x3
        for fila_bloque in range(0, 9, 3):
            for col_bloque in range(0, 9, 3):
                if random.random() < self.tasa_mutacion:
                    posiciones_editables = []

                    #Recorremos cada celda del subcuadro
                    for f in range(fila_bloque, fila_bloque + 3):
                        for c in range(col_bloque, col_bloque + 3):
                            if not self.modelo.mascara_fijas[f, c]:
                                posiciones_editables.append((f, c))
                            
                    #Intercambiamos 2 celdas aleatorias
                    if len(posiciones_editables) >= 2:
                        a, b = random.sample(posiciones_editables, 2)
                        ind[a], ind[b] = ind[b], ind[a]

        return ind

    #Ejecutamos el algoritmo genetico
    def ejecutar(self):
        #Poblacion inicial
        poblacion = self.generar_poblacion()
        historial = []

        mejor_individuo = None
        mejor_fitness = float("inf") #Fitness inicial 

        #Iteramos por generaciones
        for gen in range(self.generaciones):
            fitness_vals = [evaluar_fitness(ind) for ind in poblacion]
            idx_mejor = int(np.argmin(fitness_vals))
            mejor_actual = poblacion[idx_mejor]
            mejor_val = fitness_vals[idx_mejor]

            historial.append(mejor_val)

            print(f"Generación {gen} - Mejor fitness: {mejor_val}")

            # Actualizamos el mejor individuo encontrado
            if mejor_val < mejor_fitness:
                mejor_fitness = mejor_val
                mejor_individuo = mejor_actual.copy()

            #Si encontramos una solucion perfecta
            if mejor_val == 0:
                print("¡Sudoku resuelto!")
                return mejor_individuo, historial

            nueva_poblacion = []

            #Aplicamos elitismo (conservamos el mejor individuo)
            if self.elitismo:
                nueva_poblacion.append(mejor_actual)

            #Generamos nueva poblacion
            while len(nueva_poblacion) < self.tam_poblacion:
                p1 = self.seleccion_torneo(poblacion)
                p2 = self.seleccion_torneo(poblacion)

                hijo = self.cruce(p1, p2)
                hijo = self.mutacion(hijo)
                nueva_poblacion.append(hijo)

            poblacion = nueva_poblacion

        #Si no encontramos solucion perfecta
        print("No se encontró solución perfecta. Devolviendo mejor individuo encontrado.")
        return mejor_individuo, historial
