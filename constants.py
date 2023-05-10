BOARD_SIZE = 9
VERTICAL = 'V'
HORIZONTAL = 'H'


# action format

ROW = 'ROW'
COLUMN = 'COLUMN'
HINT = 'HINT'

CIRCLE = '◉'
RIGHT = '▶'
LEFT = '◀'
TOP = '▲'
BOTTOM = '▼'
MIDDLE = '■'
WATER = '░'

CIRCLE_D = '◉'
RIGHT_D = '▶'
LEFT_D = '◀'
TOP_D = '▲'
BOTTOM_D = '▼'
MIDDLE_D = '■'
WATER_D = '░'

DEBUG = True
EMPTY = ' '

import numpy as np
def parse_to_debug(cells: np.matrix):
    """Retorna uma string que representa o tabuleiro."""
    for row in range(BOARD_SIZE + 1):
        for col in range(BOARD_SIZE + 1):
            if str(cells[row, col]) in ["T", "t"]:
                cells[row, col] = TOP_D
            elif str(cells[row, col]) in ["B", "b"]:
                cells[row, col] = BOTTOM_D
            elif str(cells[row, col]) in ["L", "l"]:
                cells[row, col] = LEFT_D
            elif str(cells[row, col]) in ["R", "r"]:
                cells[row, col] = RIGHT_D
            elif str(cells[row, col]) in ["M", "m"]:
                cells[row, col] = MIDDLE_D
            elif str(cells[row, col]) in ["W", "w", '.']:
                cells[row, col] = WATER_D
            elif str(cells[row, col]) in ["C", "c"]:
                cells[row, col] = CIRCLE_D
            else:
                continue
    return cells
