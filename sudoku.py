import numpy as np
import copy
import tkinter as tk

class SudokuModelo:
    def __init__(self, tablero):
        self.tablero = np.array(tablero)
        self.mascara_fijas = (self.tablero != 0)

        # Compatibilidad con main.py
        self.fixed_mask = self.mascara_fijas


    # ---------------------------------------------------
    #  MÉTODOS NECESARIOS PARA EL GA
    # ---------------------------------------------------

    def obtener_tablero(self):
        """Devuelve el tablero actual."""
        return self.tablero

    def obtener_copia(self):
        """Devuelve una copia profunda del modelo."""
        return SudokuModelo(copy.deepcopy(self.tablero))

    # ---------------------------------------------------
    #  GENERACIÓN DE INDIVIDUOS
    # ---------------------------------------------------

    def generar_individuo(self):
        individuo = copy.deepcopy(self.tablero)

        for fila_ini in range(0, 9, 3):
            for col_ini in range(0, 9, 3):
                self._llenar_subcuadro(individuo, fila_ini, col_ini)

        return individuo

    def _llenar_subcuadro(self, tablero, fila_ini, col_ini):
        usados = set()
        posiciones_vacias = []

        for f in range(fila_ini, fila_ini + 3):
            for c in range(col_ini, col_ini + 3):
                if self.mascara_fijas[f, c]:
                    usados.add(tablero[f, c])
                else:
                    posiciones_vacias.append((f, c))

        disponibles = list(set(range(1, 10)) - usados)
        np.random.shuffle(disponibles)

        for (f, c), valor in zip(posiciones_vacias, disponibles):
            tablero[f, c] = valor

    # ---------------------------------------------------
    #  INTERFAZ GRÁFICA
    # ---------------------------------------------------

    def mostrar_tablero_tk(self, tablero):
        ventana = tk.Tk()
        ventana.title("Sudoku")
        ventana.configure(bg="#2b2b2b")

        titulo = tk.Label(
            ventana,
            text="SUDOKU",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#2b2b2b",
            pady=10
        )
        titulo.grid(row=0, column=0, columnspan=9)

        fuente = ("Arial", 16, "bold")

        for fila in range(9):
            ventana.grid_rowconfigure(fila + 1, weight=1)

            for col in range(9):
                ventana.grid_columnconfigure(col, weight=1)

                valor = tablero[fila][col]

                # alternar colores por subcuadro
                if (fila // 3 + col // 3) % 2 == 0:
                    color_fondo = "#ececec"
                else:
                    color_fondo = "#ffffff"

                # celdas fijas en gris
                if self.mascara_fijas[fila, col]:
                    color_fondo = "#b8b8b8"

                celda = tk.Label(
                    ventana,
                    text=str(valor),
                    width=4,
                    height=2,
                    font=fuente,
                    relief="solid",
                    borderwidth=1,
                    bg=color_fondo
                )

                celda.grid(row=fila + 1, column=col, sticky="nsew")

        ventana.mainloop()
