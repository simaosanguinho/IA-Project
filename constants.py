BOARD_SIZE = 9
ROW = 'ROW'
COLUMN = 'COLUMN'
HINT = 'HINT'
CIRCLE = '◉'
RIGHT = '▶'
LEFT = '◀'
TOP = '▲'
BOTTOM = '▼'
MIDDLE = '■'
WATER = '.'
DEBUG = True

import numpy as np
def parse_to_debug(cells: np.matrix):
    """Retorna uma string que representa o tabuleiro."""
    for row in range(BOARD_SIZE + 1):
        for col in range(BOARD_SIZE + 1):
            if str(cells[row, col]) in ["T", "t"]:
                cells[row, col] = TOP
            elif str(cells[row, col]) in ["B", "b"]:
                cells[row, col] = BOTTOM
            elif str(cells[row, col]) in ["L", "l"]:
                cells[row, col] = LEFT
            elif str(cells[row, col]) in ["R", "r"]:
                cells[row, col] = RIGHT
            elif str(cells[row, col]) in ["M", "m"]:
                cells[row, col] = MIDDLE
            elif str(cells[row, col]) in ["W", "w"]:
                cells[row, col] = WATER
            elif str(cells[row, col]) in ["C", "c"]:
                cells[row, col] = CIRCLE
            else:
                continue
    return cells
