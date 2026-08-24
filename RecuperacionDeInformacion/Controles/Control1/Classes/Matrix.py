"""
    Hecho por: armando arredondo valle
    Clase de Matriz, la vdd preferí usar POO para esto 
    pq si no sería una lata después.

"""
import numpy as np

class Matrix:
    def __init__(self, rows, cols=None):
        # Matrix(filas, columnas) -> matriz de ceros
        # Matrix(datos)           -> desde una lista de listas o un numpy array
        if cols is None:
            self.data = [list(row) for row in rows]
            self.rows = len(self.data)
            self.cols = len(self.data[0]) if self.data else 0
        else:
            self.rows = rows
            self.cols = cols
            self.data = [[0 for _ in range(cols)] for _ in range(rows)]

    def __str__(self):
        return self.display()

    __repr__ = __str__

    def to_array(self, dtype=None):
        """Devuelve los datos como numpy array (para pasarlos a las funciones de cv2/numpy)."""
        return np.array(self.data, dtype=dtype)

    def __array__(self, dtype=None, copy=None):
        """Permite usar un Matrix directamente en funciones de numpy (np.allclose, etc.)."""
        return self.to_array(dtype)

    def set_value(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.data[row][col] = value
        else:
            raise IndexError("Row or column index out of bounds.")

    def get_value(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data[row][col]
        else:
            raise IndexError("Row or column index out of bounds.")

    def display(self, decimal_places=0):
        rows = []
        for row in self.data:
            formatted_row = []
            for value in row:
                if isinstance(value, str):
                    formatted_row.append(value)
                else:
                    formatted_row.append(f"{value:.{decimal_places}f}")
            rows.append(formatted_row)

        if not rows or not rows[0]:
            return ""

        width = max(len(cell) for row in rows for cell in row)
        return "\n".join(
            " ".join(cell.rjust(width) for cell in row)
            for row in rows
        )
        