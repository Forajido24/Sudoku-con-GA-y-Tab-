import tkinter as tk
from tkinter import messagebox
from sudoku import SudokuModelo
from algoritmo_GA import AlgoritmoGeneticoSudoku


# ============================
# FUNCIÓN PARA DIBUJAR SUDOKU
# ============================
def dibujar_tablero(canvas, modelo_sudoku):
    canvas.delete("all")  # limpiar

    tablero = modelo_sudoku.tablero


    size = 40
    offset = 20

    for fila in range(9):
        for col in range(9):

            x1 = offset + col * size
            y1 = offset + fila * size
            x2 = x1 + size
            y2 = y1 + size

            # Color alternado de subcuadros
            if (fila // 3 + col // 3) % 2 == 0:
                color = "#E6F7FF"
            else:
                color = "#FFFFFF"

            # Celdas fijas en gris
            if model.fixed_mask[fila, col]:
                color = "#D3D3D3"

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

            valor = tablero[fila, col]
            if valor != 0:
                canvas.create_text(
                    x1 + size // 2,
                    y1 + size // 2,
                    text=str(valor),
                    font=("Arial", 16, "bold")
                )

    # Líneas gruesas para 3x3
    for i in range(10):
        width = 3 if i % 3 == 0 else 1
        canvas.create_line(offset, offset + i * size, offset + 9 * size, offset + i * size, width=width)
        canvas.create_line(offset + i * size, offset, offset + i * size, offset + 9 * size, width=width)


# ============================
# ACCIONES DE BOTONES
# ============================
def ejecutar_GA():
    messagebox.showinfo("Ejecutando", "Ejecutando Algoritmo Genético...")

    ga = AlgoritmoGeneticoSudoku(model)
    solucion, historial = ga.ejecutar()

    if solucion is None:
        messagebox.showwarning("Sin solución", "No se encontró solución.")
        return

    model.tablero = solucion   # ← AQUÍ EL CAMBIO CORRECTO
    dibujar_tablero(canvas, model)
    messagebox.showinfo("Listo", "¡El GA ha terminado y se actualizó el tablero!")


def limpiar_tablero():
    # OJO: sólo borro celdas NO FIJAS
    for fila in range(9):
        for col in range(9):
            if not model.fixed_mask[fila, col]:
                model.board[fila, col] = 0

    dibujar_tablero(canvas, model)


def salir():
    ventana.destroy()


# ============================
#       INTERFAZ GRÁFICA
# ============================
ventana = tk.Tk()
ventana.title("Sudoku con Algoritmo Genético")
ventana.geometry("550x600")
ventana.configure(bg="#1E1E1E")

tk.Label(
    ventana,
    text="SUDOKU",
    font=("Arial", 26, "bold"),
    bg="#1E1E1E",
    fg="white"
).pack(pady=10)

canvas = tk.Canvas(ventana, width=420, height=420, bg="#1E1E1E", highlightthickness=0)
canvas.pack()


# ============================
# CARGAR TABLERO BASE
# ============================
TABLERO_INICIAL = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

model = SudokuModelo(TABLERO_INICIAL)

dibujar_tablero(canvas, model)


# ============================
# BOTONES
# ============================
frame_botones = tk.Frame(ventana, bg="#1E1E1E")
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Ejecutar GA", font=("Arial", 14),
          bg="#4CAF50", fg="white", command=ejecutar_GA).grid(row=0, column=0, padx=10)

tk.Button(frame_botones, text="Salir", font=("Arial", 14),
          bg="#F44336", fg="white", command=salir).grid(row=0, column=2, padx=10)


ventana.mainloop()
