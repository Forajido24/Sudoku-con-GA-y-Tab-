import numpy as np
import random
from collections import deque
from funcion_fitness import evaluar_fitness

class Tabu:
    def __init__(self, modelo_sudoku, max_iter=2000, tabu_tam=300, neighborhood_size=60):
        self.model = modelo_sudoku
        self.max_iter = max_iter
        self.tabu = deque(maxlen=tabu_tam)
        self.neighborhood_size = neighborhood_size

    def _generar_candidato_swap_en_bloque(self, tablero):
        """
        Genera un candidato seleccionando un bloque aleatorio y haciendo un swap
        entre dos posiciones no fijas dentro del bloque. Devuelve (nuevo_tablero, move)
        donde move = ((r1,c1),(r2,c2))
        """
        nuevo = tablero.copy()
        fila_b = random.choice([0, 3, 6])
        col_b = random.choice([0, 3, 6])

        libres = []
        for f in range(fila_b, fila_b + 3):
            for c in range(col_b, col_b + 3):
                if not self.model.fixed_mask[f, c]:
                    libres.append((f, c))

        if len(libres) < 2:
            return nuevo, None

        a, b = random.sample(libres, 2)
        nuevo[a], nuevo[b] = nuevo[b], nuevo[a]
        move = (a, b) if a <= b else (b, a)   # ordenar para consistencia
        return nuevo, move

    def generar_vecinos(self, tablero, k=None):
        """Genera k vecinos muestreados y sus moves."""
        k = k or self.neighborhood_size
        vecinos = []
        attempts = 0
        while len(vecinos) < k and attempts < k * 4:
            attempts += 1
            vecino, move = self._generar_candidato_swap_en_bloque(tablero)
            if move is None:
                continue
            # evitar duplicados en la lista de candidatos
            # (comparamos move en vez de tablero para eficiencia)
            if any(mv == move for (_, mv) in vecinos):
                continue
            vecinos.append((vecino, move))
        return vecinos

    def ejecutar(self):
        print("Entré a Tabu con fit inicial:", evaluar_fitness(self.model.tablero))

        current = self.model.tablero.copy()
        current_fit = evaluar_fitness(current)

        best = current.copy()
        best_fit = current_fit

        # main loop
        for i in range(self.max_iter):
            # 1) generar candidatos
            candidatos = self.generar_vecinos(current)

            scored = []
            for vecino, move in candidatos:
                f = evaluar_fitness(vecino)
                scored.append((f, vecino, move))

            if not scored:
                # no se pudieron generar vecinos válidos
                break

            # 2) ordenar por fitness ascendente
            scored.sort(key=lambda x: x[0])

            # 3) seleccionar el mejor candidato permitido (no tabú o aspiración)
            seleccionado = None
            for f, vecino, move in scored:
                if move not in self.tabu:
                    seleccionado = (f, vecino, move)
                    break
                # criterio de aspiración: si mejora el mejor global, permitir
                if f < best_fit:
                    seleccionado = (f, vecino, move)
                    break

            # si ninguno fue seleccionado (raro), tomar el mejor de todos
            if seleccionado is None:
                f, vecino, move = scored[0]
                seleccionado = (f, vecino, move)

            f_sel, vecino_sel, move_sel = seleccionado

            # 4) aceptar movimiento (solo si mejora current o por exploracion controlada)
            # Aceptamos el seleccionado como nuevo current (estrategia estándar)
            current = vecino_sel
            current_fit = f_sel

            # 5) actualizar mejor global si corresponde
            if current_fit < best_fit:
                best_fit = current_fit
                best = current.copy()

            # 6) actualizar lista tabú con el move (podrías almacenar move_sel)
            self.tabu.append(move_sel)

            # 7) logging mínimo
            if i % 10 == 0 or current_fit <= best_fit + 5:
                print(f"Iteración {i}: current_fit = {current_fit} | best_fit = {best_fit}")

            # 8) parada temprana
            if best_fit == 0:
                break

        return best, best_fit
