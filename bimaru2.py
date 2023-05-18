# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from sys import stdin
import constants as const
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, rows: list, columns: list):
        self.limit_rows = rows
        self.limit_columns = columns
        self.current_rows = [0] * 10
        self.current_columns = [0] * 10

        # create matrix for the board cells
        self.cells = np.matrix([[' ' for x in range(len(rows))]
                               for y in range(len(columns))])

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if (self.valid_cell(row, col)):
            return self.cells[row, col]

    def valid_cell(self, row: int, col: int) -> bool:
        """Verifica se a célula é válida."""
        return not (row < 0 or row > const.BOARD_SIZE or col < 0 or col > const.BOARD_SIZE)

    def set_value(self, row: int, col: int, value: str) -> None:
        """Atribui o valor na respetiva posição do tabuleiro."""
        if (self.valid_cell(row, col) and self.cells[row, col] == const.EMPTY):
            self.cells[row, col] = value

            if (value not in ['W', '.']):
                self.current_rows[row] += 1
                self.current_columns[col] += 1

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col-1), self.get_value(row, col+1))

    def is_adjacent_water_horizontal(self, row: int, col: int) -> bool:
        """Verifica se a célula está adjacente a água."""
        up, down = self.adjacent_vertical_values(row, col)
        return (up in ['.', 'W'] or down in ['.', 'W'])

    def is_adjacent_water_vertical(self, row: int, col: int) -> bool:
        """Verifica se a célula está adjacente a água."""
        left, right = self.adjacent_horizontal_values(row, col)
        return (left in ['.', 'W'] or right in ['.', 'W'])

    def fill_row_with_water(self, row: int) -> None:
        """Preenche a linha 'row' com água."""
        for col in range(const.BOARD_SIZE+1):
            if (self.get_value(row, col) == const.EMPTY):
                self.set_value(row, col, '.')

    def fill_column_with_water(self, col: int) -> None:
        """Preenche a coluna 'col' com água."""
        for row in range(const.BOARD_SIZE+1):
            if (self.get_value(row, col) == const.EMPTY):
                self.set_value(row, col, '.')

    def fill_segments_with_water(self, row: int, col: int, length: int, orientation: str) -> None:
        """Preenche segmentos de água"""

        if (orientation == const.HORIZONTAL):
            for i in range(length):
                cell = self.get_value(row, col+i)
                if (cell == const.EMPTY):
                    self.set_value(row, col+i, '.')
        elif (orientation == const.VERTICAL):
            for i in range(length):
                cell = self.get_value(row+i, col)
                if (cell == const.EMPTY):
                    self.set_value(row+i, col, '.')

    def fill_exausted_rows_cols(self) -> None:
        """Preenche as linhas e colunas que já estão completas."""
        for i in range(const.BOARD_SIZE+1):
            if (self.current_rows[i] == self.limit_rows[i]):
                self.fill_row_with_water(i)
            if (self.current_columns[i] == self.limit_columns[i]):
                self.fill_column_with_water(i)

    def surround_circle(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um circulo."""
        for i in range(3):
            self.fill_segments_with_water(
                row - 1 + i, col - 1, 3, const.HORIZONTAL)

    def surround_top(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um top."""
        for i in range(3):
            if (i == 1):
                self.fill_segments_with_water(
                    row - 1, col, 1, const.VERTICAL)
            else:
                self.fill_segments_with_water(
                    row - 1, col - 1 + i, 4, const.VERTICAL)

    def surround_bottom(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um bottom."""
        for i in range(3):
            if (i == 1):
                self.fill_segments_with_water(
                    row + 1, col, 1, const.VERTICAL)
            else:
                self.fill_segments_with_water(
                    row - 2, col - 1 + i, 4, const.VERTICAL)

    def surround_left(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um left. """
        for i in range(3):
            if (i == 1):
                self.fill_segments_with_water(
                    row, col - 1, 1, const.HORIZONTAL)
            else:
                self.fill_segments_with_water(
                    row - 1 + i, col - 1, 4, const.HORIZONTAL)

    def surround_right(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um right. """ 
        for i in range(3):
            if (i == 1):
                self.fill_segments_with_water(
                    row, col + 1, 1, const.HORIZONTAL)
            else:
                self.fill_segments_with_water(
                    row - 1 + i, col - 2, 4, const.HORIZONTAL)

    def surround_middle(self, row: int, col: int) -> None:
        """ Preenche os segmentos de água em volta de um middle. """
        if (self.is_adjacent_water_vertical(row, col)):
            self.fill_segments_with_water(
                row - 2, col - 1, 5, const.VERTICAL)
            self.fill_segments_with_water(
                row - 2, col + 1, 5, const.VERTICAL)
        elif (self.is_adjacent_water_horizontal(row, col)):
            self.fill_segments_with_water(
                row - 1, col - 2, 5, const.HORIZONTAL)
            self.fill_segments_with_water(
                row + 1, col - 2, 5, const.HORIZONTAL)

    def surround_hint(self, row: int, col: int, value: str) -> None:
        """ Preenche os segmentos de água em volta de uma hint. """
        match value:
            case 'C':
                self.surround_circle(row, col)
            case 'T':
                self.surround_top(row, col)
            case 'B':
                self.surround_bottom(row, col)
            case 'R':
                self.surround_right(row, col)
            case 'L':
                self.surround_left(row, col)
            case 'M':
                self.surround_middle(row, col)

    @staticmethod
    def parse_instance() -> None:
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """
        rows = []
        columns = []
        hints = []

        while True:
            instance = stdin.readline().split()
            line = [int(x) if x.isdigit() else x for x in instance]
            if not line:
                break

            match line[0]:
                case const.ROW:
                    rows = line[1:]
                case const.COLUMN:
                    columns = line[1:]
                case const.HINT:
                    hints.append(line[1:])
                case _:
                    continue

        new_board = Board(rows, columns)
        # add hints
        for hint in hints:
            row, col, value = hint[0], hint[1], hint[2]
            new_board.set_value(row, col, value)
        # fill obvious rows/cols with water
        new_board.fill_exausted_rows_cols()
        # surround hints with water
        for hint in hints:
            row, col, value = hint[0], hint[1], hint[2]
            new_board.surround_hint(row, col, value)

        return new_board

    def __str__(self):
        """Retorna uma string que representa o tabuleiro."""
        if not const.DEBUG:
            return str(self.cells)
        else:
            return str(const.parse_to_debug(self.cells))


class Bimaru(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance()
    # Criar uma instância de Takuzu:
    problem = Bimaru(board)
    print(board)

    # Obter o nó solução usando a procura em profundidade:
    """ goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    if goal_node:
        print(goal_node.state)
    else:
        print("No solution found") """
