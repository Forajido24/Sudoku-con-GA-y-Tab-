import numpy as np
import copy

#Representa el modelo del Sudoku
class SudokuModelo:
    def __init__(self, tablero):
        self.tablero = np.array(tablero)
        self.mascara_fijas = (self.tablero != 0)
        self.fixed_mask = self.mascara_fijas  #Union con el main

    #Devuelve el tablero actual
    def obtener_tablero(self):
        return self.tablero

    #Devuelve una copia del modelo
    def obtener_copia(self):
        return SudokuModelo(copy.deepcopy(self.tablero))

    #Genera un individuo válido llenando los subcuadros
    def generar_individuo(self):
        individuo = copy.deepcopy(self.tablero)
        for fila_ini in range(0, 9, 3):
            for col_ini in range(0, 9, 3):
                self._llenar_subcuadro(individuo, fila_ini, col_ini)
        return individuo

    #Llenar un subcuadro 3x3 con numeros validos
    def _llenar_subcuadro(self, tablero, fila_ini, col_ini):
        usados = set()
        posiciones_vacias = []

        for f in range(fila_ini, fila_ini + 3):
            for c in range(col_ini, col_ini + 3):
                if self.mascara_fijas[f, c]:
                    #Si ya hay un numero lo marcamos como usado
                    usados.add(tablero[f, c])
                else:
                    #Si esta vacio guardamos la posicion
                    posiciones_vacias.append((f, c))

        #Numeros del 1-9 no usados en el subcuadro
        disponibles = list(set(range(1, 10)) - usados)
        np.random.shuffle(disponibles)

        #Asignar numeros disponibles a las posiciones vacias
        for (f, c), valor in zip(posiciones_vacias, disponibles):
            tablero[f, c] = valor
