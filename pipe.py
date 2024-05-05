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
        self.remaining_pecas = []
    
    def print(self):
        board_string = "\n".join([" ".join(row) for row in self.matrix])
        return board_string
    
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
        new_board.remaining_pecas = self.remaining_pecas
        return new_board



    def calculate_state(self):
        """Calcula os valores do estado interno, para ser usado
        no tabuleiro inicial."""
        self.remaining_pecas = []

        # Store which positions can be placed for each cell
        self.possible_moves = ()

        for col in range(self.size):
            possibilities = ()
            for row in range(self.size):
                if (col == 0 and (row == 0 or row == self.size - 1)) or (col == self.size - 1 and (row == 0 or row == self.size - 1)):
                    if  self.matrix[row][col][0] == "B" or self.matrix[row][col][0] == "L":
                        self.invalid = True
                        return self
                    elif self.matrix[row][col][0] == "V":
                        if (col == 0 and row == 0):
                            possibilities += ((),)
                            self.set_cell(row, col,"VB")
                        elif (col == self.size - 1 and row == 0):
                            possibilities += ((),)
                            self.set_cell(row, col,"VE")
                        elif (col == 0 and row == self.size - 1):
                            possibilities += ((),)
                            self.set_cell(row, col,"VD")
                        elif (col == self.size - 1 and row == self.size - 1):
                            possibilities += ((),)
                            self.set_cell(row, col,"VC")
                    else:
                        self.remaining_pecas.append((row, col))

                elif row == 0:
                    if self.matrix[row][col][0] == "B":
                        possibilities += ((),)
                        self.set_cell(row, col,"BB")
                    elif self.matrix[row][col][0] == "L":
                        possibilities += ((),)
                        self.set_cell(row, col,"LH")
                elif row == self.size - 1:
                    if self.matrix[row][col][0] == "B":
                        possibilities += ((),)
                        self.set_cell(row, col,"BC")
                    elif self.matrix[row][col][0] == "L":
                        possibilities += ((),)
                        self.set_cell(row, col,"LH")

                elif col == 0:
                    if self.matrix[row][col][0] == "B":
                        possibilities += ((),)
                        self.set_cell(row, col,"BD")
                    elif self.matrix[row][col][0] == "L":
                        possibilities += ((),)
                        self.set_cell(row, col,"LV")
                elif col == self.size - 1:
                    if self.matrix[row][col][0] == "B":
                        possibilities += ((),)
                        self.set_cell(row, col,"BE")
                    elif self.matrix[row][col][0] == "L":
                        possibilities += ((),)
                        self.set_cell(row, col,"LV")
                else:   
                    possibilities_aux = tuple(self.actions_for_cell(row, col))
                    possibilities += (possibilities_aux,)
                    self.remaining_pecas.append((row, col))

            self.possible_moves += (possibilities,)

        return self
    """      
        for row in range(self.size):
            zero_count, one_count = 0, 0
            for col in range(self.size):
                if self.cells[row][col] == 0:
                    zero_count += 1
                elif self.cells[row][col] == 1:
                    one_count += 1
            self.row_counts += ((fecho, bifurcacao, volta, ligacao),)

        for row in range(self.size):
            row_possibilities = ()
            for col in range(self.size):
                if self.cells[row][col] != 2:
                    row_possibilities += ((),)
                    continue
                possibilities = tuple(self.actions_for_cell(row, col))
                row_possibilities += (possibilities,)
                if len(possibilities) == 2:
                    self.count_pos_with_two_actions += 1
                    self.remaining_cells.append((row, col))
                elif len(possibilities) == 0:
                    # If it's impossible to complete a board,
                    # abort immediately to save computing costs
                    self.invalid = True
                    return self
                else:
                    # Insert cells with only one possibility at the front
                    # of the list, so they're placed first, reducing the
                    # branching factor
                    self.remaining_cells.insert(0, (row, col))
            self.possible_moves += (row_possibilities,)

        return self
    """
    def set_cell(self, row, col, position):
        new_matrix = [row[:] for row in self.matrix]  # Create a new copy of the matrix
        new_matrix[row][col] = position
        new_board = Board(new_matrix)
        # Carry over other attributes
        new_board.remaining_pecas = self.remaining_pecas[:]
        # Add any additional attributes you need to transfer
        return new_board
    
    def actions_for_cell(self, row, col):
        """ A maneira como esta organizado com os if's pode ser alterada no futuro
            para nao haver a parte dos if's com move[1], mas por enquanto deixamos
            assim e depois vemos """
        move = self.matrix[row][col]
        vertical_move = self.adjacent_vertical_values(row, col)
        horizontal_move = self.adjacent_horizontal_values(row, col)
        acceptable_up_conections = ()
        acceptable_down_conections = ()
        acceptable_right_conections = ()
        acceptable_left_conections = ()
        if move[0] == "F":
            if move[1] == "C":
                acceptable_up_connections = ("BB", "BE","BD","VB", "VE", "LV")
            elif move[1] == "B":
                acceptable_down_conections  = ("BC", "BE", "BD", "VC", "VD", "LV")
            elif move[1] == "E":
                acceptable_left_conections = ("BC", "BB", "BD", "VB", "VD", "LH")
            elif move[1] == "D":
                acceptable_right_conections = ("BC", "BB", "BE", "VC", "VE", "LH")
        elif move[0] == "B":
            if move[1] == "C":
                acceptable_up_conections = ("FB", "BB", "BE", "BD", "VB", "VE", "LV")
                acceptable_right_conections = ("FE", "BC", "BE", "BB","VC", "VE", "LH")
                acceptable_left_conections = ("FD", "BC", "BD", "BB", "VB", "VD", "LH")
            if move[1] == "B":
                acceptable_down_conections = ("FC", "BC", "BE", "BD", "VC", "VD", "LV")
                acceptable_right_conections = ("FE", "BC", "BE", "BB","VC", "VE", "LH")
                acceptable_left_conections = ("FD", "BC", "BD", "BB", "VB", "VD", "LH")
            if move[1] == "E":
                acceptable_down_conections = ("FC", "BC", "BE", "BD", "VC", "VD", "LV")
                acceptable_up_conections = ("FB", "BB", "BE", "BD", "VB", "VE", "LV")
                acceptable_left_conections = ("FD", "BC", "BD", "BB", "VB", "VD", "LH")
            if move[1] == "D":
                acceptable_down_conections = ("FC", "BC", "BE", "BD", "VC", "VD", "LV")
                acceptable_right_conections = ("FE", "BC", "BE", "BB","VC", "VE", "LH")
                acceptable_up_conections = ("FB", "BB", "BE", "BD", "VB", "VE", "LV")
        elif move[0] == "V":
            if move[1] == "C":
                acceptable_up_connections = ("FB", "BB", "BE", "BD", "VB","VE", "LV")
                acceptable_left_conections = ("FD", "BC", "BB", "BD", "VB", "VD", "LH")
            elif move[1] == "B":
                acceptable_right_conections = ("FE", "BC", "BB", "BE", "VC", "VE", "LH")
                acceptable_down_conections = ("FC", "BE", "BC", "BD", "VC", "VD", "LV")
            elif move[1] == "E":
                acceptable_left_conections = ("FD", "BC", "BB", "BD", "VB","VD", "LH")
                acceptable_down_conections = ("FC", "BC", "BE", "BD", "VC", "VD", "LV")
            elif move[1] == "D":
                acceptable_right_conections = ("FE", "BC", "BB", "BE", "VC", "VE","LH")
                acceptable_up_conections = ("FB", "BB", "BE", "BD", "VB", "VE", "LV")
        elif move[0] == "L":
            if move[1] == "H":
                acceptable_left_conections = ("FD", "BC", "BB", "BD","VD", "VB", "LH")
                acceptable_right_conections = ("FE", "BC", "BB", "BE", "VC", "VE", "LH")
            elif move[1] == "V":
                acceptable_up_conections = ("FB", "BB", "BE", "BD", "VE", "VB", "LV")
                acceptable_down_conections = ("FC", "BC", "BE", "BD", "VC", "VD", "LV")
        return (acceptable_up_conections, acceptable_right_conections, acceptable_left_conections, acceptable_down_conections)
  
    def check_frontiers(self, row, col):
        move = self.matrix[row][col]
        if row == 0 and col == 0:
            if move[0] == "F":
                return ("FD","FB")
        elif row == 0 and col == self.size - 1:
            if move[0] == "F":
                return ("FB","FE")
        elif row == self.size - 1 and col == 0:
            if move[0] == "F":
                return ("FC","FD")
        elif row == self.size - 1 and col == self.size - 1:
            if move[0] == "F":
                return ("FC","FE")
        elif col == 0:
            if move[0] == "F":
                return ("FB","FC","FD")
            elif move[0] == "V":
                return ("VB","VD")
        elif col == self.size - 1:
            if move[0] == "F":
                return ("FB","FC","FE")
            elif move[0] == "V":
                return ("VC","VE")
        elif row == 0:
            if move[0] == "F":
                return ("FB","FE","FD")
            elif move[0] == "V":
                return ("VB","VE")
        elif row == self.size - 1:
            if move[0] == "F":
                return ("FC","FE","FD")
            elif move[0] == "V":
                return ("VC","VD")
        else:
            if move[0] == "F":
                return ("FC","FB","FE","FD")
            elif move[0] == "B":
                return ("BC","BB","BE","BD")
            elif move[0] == "V":
                return ("VC","VB","VE","VD")
            elif move[0] == "L":
                return ("LH","LV")

    
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        # TODO
        return self.matrix[row][col]

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
    
    def get_remaining_pecas_count(self):
        """Devolve o número de posições em branco"""
        return len(self.remaining_pecas)

    def calculate_next_possible_moves(self, row: int, col: int):
        """Recebe a posição que foi alterada, de forma a atualizar os valores
        possíveis para as posições afetadas"""

        # Recalculate for affected row and column
        new_possible_moves = ()
        for r in range(self.size):
            row_possibilities = ()
            for c in range(self.size):
                old_possibilities = self.get_possibilities_for_peca(r, c)
                if (r != row and c != col) or len(old_possibilities) == 0:
                    row_possibilities += (old_possibilities,)
                    continue

                possibilities = tuple(self.actions_for_cell(r, c))

                if (r != row or c != col) and len(possibilities) == 0:
                    self.invalid = True
                    return

                if len(old_possibilities) == 2 and len(possibilities) < 2:
                    self.count_pos_with_two_actions -= 1
                    if not (r == row and c == col):
                        self.remaining_cells.remove((r, c))
                        self.remaining_cells.insert(0, (r, c))

                row_possibilities += (possibilities,)

            new_possible_moves += (row_possibilities,)

        self.possible_moves = new_possible_moves
    def get_possibilities_for_peca(self, row, col):
        return self.possible_moves[row][col]

    @staticmethod
    def parse_instance():

        matrix = []
        for line in sys.stdin:
            row = line.strip().split()
            matrix.append(row)
        return Board(matrix).calculate_state()

        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """

    # TODO: outros metodos da classe




class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = PipeManiaState(board)
        super().__init__(state)
        pass

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento.
        if state.board.invalid or state.board.get_remaining_cells_count() == 0:
            return []

        row, col = state.board.get_next_cell()

        possibilities = state.board.get_possibilities_for_cell(row, col)
        return map(lambda number: (row, col, number), possibilities)"""
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state).
        (row, col, value) = action
        return PipeManiaState(state.board.set_number(row, col, value))"""
        (row, col, direcao) = action
        return PipeManiaState(state.board.rodar_peça(row, col, direcao))

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return state.board.get_remaining_pecas_count() == 0

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*.
        board = node.state.board
        return board.count_pos_with_two_actions"""
        pass


if __name__ == "__main__":
    board = Board.parse_instance()
    initial_state = PipeManiaState(board)
    print(initial_state.board.get_value(0, 0))
    second = initial_state.board.calculate_state()
    print(second.get_value(0, 0))
    """
    goal_node = greedy_search(takuzu)
    print(goal_node.state.board)
    pass
    """

