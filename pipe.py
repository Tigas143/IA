# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, matrix):
        self.matrix = matrix
        self.size = len(matrix)
        self.invalid = False

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO
        return self.matrix[row][col]
    def rodar_peça(self, row: int, col: int, direçao: bool):
        """Devolve um novo Board com a peça na nova posição"""
        peça = self.matrix[row][col]
        move = ""
        if peça[1] == "C":
            if direçao:
                move = "D"
            else:
                move = "E"
        elif peça[1] == "B":
            if direçao:
                move = "E"
            else:
                move = "D"
        elif peça[1] == "E":
            if direçao:
                move = "C"
            else:
                move = "B"
        elif peça[1] == "D":
            if direçao:
                move = "B"
            else:
                move = "C"
        elif peça[1] == "H":
            move = "V"
        elif peça[1] == "V":
            move = "H"
        new_matrix = self.matrix
        new_matrix[row][col] = peça[0]+move
        new_board = Board(new_matrix)
        return new_board


        
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente. """
        if row - 1 < 0 and row + 1 >= len(self.matrix):
            return (None, None)  # Retorna None se não houver vizinhos válidos
        elif row - 1 < 0 :
            return (None, self.matrix[row + 1][col])
        elif row + 1 >= len(self.matrix):
            return (self.matrix[row - 1][col], None) 
        else:
            return (self.matrix[row - 1][col], self.matrix[row + 1][col])

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente. """
        if col - 1 < 0 and col + 1 >= len(self.matrix):
            return (None, None)  # Retorna None se não houver vizinhos válidos
        elif col - 1 < 0 :
            return (None, self.matrix[row][col + 1])
        elif col + 1 >= len(self.matrix):
            return (self.matrix[row][col - 1], None) 
        else:
            return (self.matrix[row][col - 1], self.matrix[row][col + 1])

    @staticmethod
    def parse_instance():
        matrix = []
        for line in sys.stdin:
            row = line.strip().split()
            matrix.append(row)
        return Board(matrix)

        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = PipeManiaState(board)
        super().__init__(state)
        pass

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row, col, direcao) = action
        return PipeManiaState(state.board.rodar_peça(row, col, direcao))
        pass

    def goal_test(self, state: PipeManiaState):
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
    pass

# Ler grelha do figura 1a:
board = Board.parse_instance()
# Criar uma instância de PipeMania:
problem = PipeMania(board)
# Criar um estado com a configuração inicial:
initial_state = PipeManiaState(board)
# Mostrar valor na posição (2, 2):
print(initial_state.board.get_value(2, 2))
# Realizar ação de rodar 90° clockwise a peça (2, 2)
result_state = problem.result(initial_state, (2, 2, True))
# Mostrar valor na posição (2, 2):
print(result_state.board.get_value(2, 2))



