import numpy as np
import copy

class SudokuModel:
    def __init__(self, board):
        """
        board: matriz 9x9 con ceros en las celdas vacías.
        """
        self.board = np.array(board)
        self.fixed_mask = (self.board != 0)  # True = celda fija

    # ---------------------------------------------------
    # 1. GENERAR INDIVIDUO INICIAL VÁLIDO (POR SUBCUADROS)
    # ---------------------------------------------------
    def generate_individual(self):
        """
        Devuelve un Sudoku completo respetando:
        - Celdas fijas
        - Subcuadros 3x3 correctos (sin repeticiones)
        Corrige solo subcuadros; filas/columnas se corrigen con GA.
        """
        individual = copy.deepcopy(self.board)

        # Llenar cada subcuadro con números válidos
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                self._fill_subgrid(individual, br, bc)

        return individual

    # -------------------------------------------
    # LLENAR UN SUBCUADRO 3×3 RESPETANDO FIJOS
    # -------------------------------------------
    def _fill_subgrid(self, board, start_row, start_col):
        """
        Llena un subcuadro 3x3 con números del 1 al 9
        sin repetir, respetando las celdas fijas.
        """
        used = set()
        empty_positions = []

        # Revisar el subcuadro
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.fixed_mask[r, c]:
                    used.add(board[r, c])
                else:
                    empty_positions.append((r, c))

        # Números disponibles
        available = list(set(range(1, 10)) - used)
        np.random.shuffle(available)

        # Llenar las celdas vacías
        for pos, value in zip(empty_positions, available):
            r, c = pos
            board[r, c] = value

    # -------------------------------------------------
    # 2. UTILIDAD: IMPRIMIR EL TABLERO BONITO (OPCIONAL)
    # -------------------------------------------------
    def print_board(self, board):
        print("\n-------------------------")
        for i in range(9):
            row = ""
            for j in range(9):
                num = board[i][j]
                row += f" {num if num != 0 else '.'}"
                if (j + 1) % 3 == 0 and j < 8:
                    row += " |"
            print(row)
            if (i + 1) % 3 == 0 and i < 8:
                print("-------------------------")
        print("-------------------------")


