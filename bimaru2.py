# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

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
        else:
            return None

    def valid_cell(self, row: int, col: int) -> bool:
        """Verifica se a célula é válida."""
        return not (row < 0 or row > const.BOARD_SIZE or col < 0 or col > const.BOARD_SIZE)

    def set_value(self, row: int, col: int, value: str):
        """Atribui o valor na respetiva posição do tabuleiro."""
        if (self.valid_cell(row, col) and self.cells[row, col] == const.EMPTY):
            self.cells[row, col] = value
            
            if(value not in ['W', '.']):
                self.current_rows[row] += 1
                self.current_columns[col] += 1
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
    
    def fill_row_with_water(self, row: int):
        """Preenche a linha 'row' com água."""
        for col in range(const.BOARD_SIZE+1):
            if(self.get_value(row, col) == const.EMPTY):
                self.set_value(row, col, '.')
    
    def fill_column_with_water(self, col: int): 
        """Preenche a coluna 'col' com água."""
        for row in range(const.BOARD_SIZE+1):
            if(self.get_value(row, col) == const.EMPTY):
                self.set_value(row, col, '.')

    def fill_segments_with_water(self, row: int, col: int, length: int, orientation: str):
        """Preenche os segmentos de água adjacentes à posição (row, col)."""
        
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
    
    def fill_exausted_rows_cols(self):
        """Preenche as linhas e colunas que já estão completas."""
        for i in range(const.BOARD_SIZE+1):
            if(self.current_rows[i] == self.limit_rows[i]):
                self.fill_row_with_water(i)
            if (self.current_columns[i] == self.limit_columns[i]):
                self.fill_column_with_water(i)

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
            
        board = Board(rows, columns)
        
        # add hints
        for hint in hints:
            row, col, value = hint[0], hint[1], hint[2]
            board.set_value(row, col, value)
        
        # fill obvious rows/cols with water   
        board.fill_exausted_rows_cols()
        
        # surround hints with water
        for hint in hints:
            row, col, value = hint[0], hint[1], hint[2]
            # circle hint
            if (value == 'C'):
                for i in range(3):
                    board.fill_segments_with_water(row - 1 + i, col - 1, 3, const.HORIZONTAL)
            # top hint
            if (value == 'T'):
                for i in range(3):
                    if (i == 0):
                        board.fill_segments_with_water(row - 1 + i, col - 1, 3, const.HORIZONTAL)
                    else:
                        board.fill_segments_with_water(row - 1 + i, col - 1, 1, const.HORIZONTAL)
                        board.fill_segments_with_water(row - 1 + i, col + 1, 1, const.HORIZONTAL)

            # bottom hint
            if  (value == 'B'):
                for i in range(3):
                    if (i == 2):
                        board.fill_segments_with_water(row - 1 + i, col - 1, 3, const.HORIZONTAL)
                    else:
                        board.fill_segments_with_water(row - 1 + i, col - 1, 1, const.HORIZONTAL)
                        board.fill_segments_with_water(row - 1 + i, col + 1, 1, const.HORIZONTAL)
                    
                
            # middle hint
            adjacent_water= [('.', '.'), ('.', 'None'), ('None', '.'), ('.',' '), (' ', '.')]
            
            if (value == 'M'):
                print(board.adjacent_horizontal_values(row, col))
                if (board.adjacent_horizontal_values(row, col) in adjacent_water):
                    board.fill_segments_with_water(row - 2, col - 1, 5, const.VERTICAL)
                    board.fill_segments_with_water(row - 2, col + 1, 5, const.VERTICAL)
                elif (board.adjacent_vertical_values(row, col) in adjacent_water):
                    board.fill_segments_with_water(row - 1, col - 2, 5, const.HORIZONTAL)
                    board.fill_segments_with_water(row + 1, col - 2, 5, const.HORIZONTAL)
     
        return board
    

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
    
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    # Criar um estado com a configuração inicial:
    
    initial_state = BimaruState(board)

    print(initial_state.board)