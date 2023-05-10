# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 23:
# 102082 Simão Sanguinho
# 103252 José Pereira

import sys
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

    def __init__(self, rows: list, columns: list, hints: list):
        self.rows = rows
        self.columns = columns
        self.hints = hints

        # create matrix for the board cells
        self.cells = np.matrix([[' ' for x in range(len(rows))]
                               for y in range(len(columns))])
        # add hints
        for hint in hints:
            self.cells[hint[0], hint[1]] = hint[2]
            if (hint[2] == 'W'):
                continue
            # update values for rows and columns
            self.rows[hint[0]] -= 1
            self.columns[hint[1]] -= 1

    
        print(rows, columns)
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if (self.valid_cell(row, col)):
            return self.cells[row, col]
        else:
            return None

    def valid_cell(self, row: int, col: int) -> bool:
        """Verifica se a célula é válida."""
        return not (row < 0 or row > const.BOARD_SIZE or col < 0 or col > const.BOARD_SIZE)

    def set_value(self, row: int, col: int, value: str):
        """Atribui o valor na respetiva posição do tabuleiro."""
        if (self.valid_cell(row, col)):
            self.cells[row, col] = value
        else:
            return

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col-1), self.get_value(row, col+1))

    def do_action(self, action):
        """Executa a ação de colocar um barco na posição (row, col) com
        orientação 'orientation' e tamanho 'size'."""

        row, col, value, size, orientation = action[0], action[1], \
            action[2], action[3] == const.EMPTY, action[4]

        if (orientation == const.HORIZONTAL):
            for i in range(size+1):
                if (self.get_value(row, col+i) == const.EMPTY):
                    self.set_value(row, col+i, value)
        elif (orientation == const.VERTICAL):
            for i in range(size+1):
                if (self.get_value(row+i, col) == const.EMPTY):
                    self.set_value(row+i, col, value)
        
        else:
            return

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        rows = []
        columns = []
        hints = []
        while True:
            instance = stdin.readline().split()
            line = [int(x) if x.isdigit() else x for x in instance]
            if not line:
                break

            if (line[0] == const.ROW):
                rows = line[1:]

            elif (line[0] == const.COLUMN):
                columns = line[1:]

            elif (line[0] == const.HINT):
                hints.append(line[1:])

            else:
                continue

        return Board(rows, columns, hints)

    def __str__(self):
        """Retorna uma string que representa o tabuleiro."""
        if not const.DEBUG:
            return str(self.cells)
        else:
            return str(const.parse_to_debug(self.cells))

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        board = state.board
        actions = []

        # MAYBE MERGE BOTH LOOPS INTO ONE
        # any row with 0
        for row in range(const.BOARD_SIZE + 1):
            if (board.rows[row] == 0):
                actions.append([row, 0, '.', const.BOARD_SIZE, const.HORIZONTAL])

        # any column with 0
        for col in range(const.BOARD_SIZE + 1):
            if (board.columns[col] == 0):
                actions.append([0, col, '.', const.BOARD_SIZE, const.VERTICAL])

        # MARK CELL AFTER SURROUNDED
        # fill the cells around an non water/empty cell with water
        for row in range(const.BOARD_SIZE + 1):
            for col in range(const.BOARD_SIZE + 1):
                # circle
                if (board.get_value(row, col) == CIRCLE):
                    actions.append([row-1, col-1, '.', 3, const.HORIZONTAL])
                    actions.append([row-1, col-1, '.', 3, const.VERTICAL])
                    actions.append([row-1, col+1, '.', 3, const.HORIZONTAL])
                    actions.append([row+1, col-1, '.', 3, const.VERTICAL])
        
                # top
                if(board.get_value(row, col) == TOP):
                    actions.append([row-1, col-1, '.', 3, const.HORIZONTAL])
                    actions.append([row-1, col-1, '.', 4, const.VERTICAL])
                    actions.append([row-1, col+1, '.', 4, const.VERTICAL])
                    actions.append([row+1, col, '.', 1, const.HORIZONTAL])
                
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        

        board = state.board
        board.do_action(action)
        return BimaruState(board)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return all(x == 0 for x in state.board.rows) and all(x == 0 for x in state.board.columns)

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
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    # Criar um estado com a configuração inicial:
    
    initial_state = BimaruState(board)

    actions = problem.actions(initial_state)
    for action in actions:
        initial_state = problem.result(initial_state, action)

    
    print(initial_state.board)
