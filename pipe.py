# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

"""
    É preciso arranjar uma maneira mais bonnita de so dar cet_cell no rodar_peca (eu pus no
possible_values uma string tipo "0XX" para indicar que só há 1 possibilidade para encaixar com o que
ja estava no codigo, it works, mas nao é boa pratica de certeza)
    Ter em atençao a parte do remaining_cells estar ordenado por possibilidades, atualmente 
põe-se o nó no final sem ter em atencao a quantidade de possibilidades, mas as funçoes que
usei para por as pecas ordenadas do remaining_cells no remove_possibilities partem do pressuposto que essa lista 
esta ordenada, portanto ate agora nao deu erro porque nao apareceu nenhuma exercicio, mas vai dar erro eventualmente
    No rodar_peca fazemos:
      if len(self.possible_moves[(row, col)]) == 1 or self.possible_moves[(row, col)][0] == "0":
        *retira a celula do remaining_cells, entre outras coisas*
      else:
        *poe a celula no final do remaing_cells, entre outras coisas*
    e só depois disso fazemos o calcula_next_moves, e isto não faz muito sentido tendo em conta que como o
    calcula_next_moves so calcula os moves adjacentes de Z e pode haver alguma celula X adjacente Z que por exemplo fica
    com apenas 1 possibilidade e isto pode afetar outra celula Y adjacente a X que tendo em conta esse cenário
    tambem ficaria com apenas 1 possibilidade, sendo assim no rodar peça iriamos por uma celula X que tecnicamente so tem 1 possibilidade
    no final do remaining_cells, o que é desnecessário
    Portanto faria mais sentido adaptar o calcula_next_moves a alterar as possibilidades adjacentes de todas as celulas
    que possam ter ficado com a sua possibilidade a 1
"""

import getpass
import sys
import bisect
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
        depth_diff = (
            self.board.get_remaining_pecas_count()
            - other.board.get_remaining_pecas_count()
        )

        if depth_diff != 0:
            return depth_diff < 0

        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, matrix):
        self.matrix = matrix
        self.size = len(matrix)
        self.remaining_pecas = []
        self.count_actions = 0
        self.invalid = False
    
    def print(self):
        board_string = "\n".join(["\t".join(row) for row in self.matrix])
        return board_string


    def breakpoint(self):
        getpass.getpass("Pressione Enter para continuar... (Ctrl+C para sair)")
    
    
    def rodar_peça(self, row: int, col: int, peca: str):

        #print("rodar peca:", peca, "row: ", row, "col: ", col)
        #self.breakpoint()
       
        new_matrix = [row[:] for row in self.matrix]  # Creating a deep copy of the matrix
        new_matrix[row][col] = peca
       #print("Pecas para rodar:",self.remaining_pecas)
        #print("roda peca: ", row,col, peça)

        #self.breakpoint()
        new_board = Board(new_matrix)
        new_board.count_actions = self.count_actions
        new_board.possible_moves = self.possible_moves
        if len(self.possible_moves[(row, col)]) == 1 or self.possible_moves[(row, col)][0] == "0":
            move = self.possible_moves[(row, col)][1:]
            self.count_actions -= 1
            new_board.set_cell(row, col, move)
            new_board.possible_moves[(row, col)] = ()
            new_board.remaining_pecas = self.remaining_pecas[1:]
            """
            print("\n")
            print("if", row, col)
            print("if self.remaining_pecas", self.remaining_pecas)
            print("if new_board.remaining_pecas", new_board.remaining_pecas)
            """
            
        else:
            #with open('saida.txt', 'w') as arquivo:
            # Redireciona a saída do método print para o arquivo
            #    arquivo.write(self.print())
            #exit()
            self.remaining_pecas.remove((row, col))
            num_possibilities = len(self.possible_moves[(row, col)])
            pos_to_insert = bisect.bisect_right([len(self.possible_moves[pos]) for pos in self.remaining_pecas], num_possibilities)
            #new_remaining_pecas = self.remaining_pecas[1:] + [first_element]
            self.remaining_pecas.insert(pos_to_insert, (row, col))
            new_board.remaining_pecas = self.remaining_pecas
            """
            print("\n")
            print("else", row, col)
            print("else self.remaining_pecas", self.remaining_pecas)
            print("else new_board.remaining_pecas", new_board.remaining_pecas)
            """

        #print("novo remaining_pecas", new_board.remaining_pecas)
        #print("dicionario do novo remaing_pecas", self.possible_moves)
        #print(row, col)
        #print("new_board", new_board.remaining_pecas)
        #print("self_board", self.remaining_pecas)
        new_board.calculate_next_possible_moves(row, col)
        #print("remaining_pecas apos calculate_next_possible_moves ", new_board.remaining_pecas)
        #print("dicionario apos calculate_next_possible_moves", self.possible_moves)
        return new_board
    """
    def remove_possibilities_adjacencies(self, row: int, col: int):
        values = () 
        if (row + 1, col) in self.remaining_pecas:
            self.remove_possibilities(row + 1, col)
            if self.possible_moves[(row + 1, col)] == "0":
                values += (1,)
        elif (row - 1, col) in self.remaining_pecas:
            self.remove_possibilities(row - 1, col)
            if self.possible_moves[(row - 1, col)] == "0":
                values += (2,)
        elif (row, col + 1) in self.remaining_pecas:
            self.remove_possibilities(row, col + 1)
            if self.possible_moves[(row, col + 1)] == "0":
                values += (3,)
        elif (row, col - 1) in self.remaining_pecas:
            self.remove_possibilities(row, col - 1)
            if self.possible_moves[(row, col - 1)] == "0":
                values += (4,)
    """

    def calculate_next_possible_moves(self, row: int, col: int):

        """Recebe a posição que foi alterada, de forma a atualizar as possibilidades
        das peças para as posições afetadas"""  

        if (row, col) in self.remaining_pecas:
            self.remove_possibilities(row, col)
        if (row + 1, col) in self.remaining_pecas:
            self.remove_possibilities(row + 1, col)
        if (row - 1, col) in self.remaining_pecas:
            self.remove_possibilities(row - 1, col)
        if (row, col + 1) in self.remaining_pecas:
            self.remove_possibilities(row, col + 1)
        if (row, col - 1) in self.remaining_pecas:
            self.remove_possibilities(row, col - 1)


    def calculate_state(self):
        """Calculate the values of the internal state to be used
        in the initial board."""
        self.remaining_pecas = []
        
        # Store possibilities for each cell in a dictionary
        self.possible_moves = {}
        self.count_actions = 0
        
        for row in range(self.size):
            for col in range(self.size):
                possibility = ()
                possibility = self.check_frontiers(row, col)
                num_possibilities = len(possibility)
                self.count_actions += num_possibilities

                if num_possibilities == 1:
                    self.set_cell(row, col, possibility[0])
                    self.count_actions -= 1
                    self.possible_moves[(row, col)] = ()

                elif num_possibilities != 4:
                    self.possible_moves[(row, col)] = possibility

                    if self.remaining_pecas:
                        pos_to_insert = bisect.bisect_right([len(self.possible_moves[pos]) for pos in self.remaining_pecas], num_possibilities)
                        self.remaining_pecas.insert(pos_to_insert, (row, col))
                    else:
                        self.remaining_pecas.insert(0, (row, col))

                else:
                    self.possible_moves[(row, col)] = possibility
                    self.remaining_pecas.append((row, col))

        values = 1   
        hi = ()
        lenght = len(self.remaining_pecas)
        while values == 1:
            aux = 0
            for (row,col) in self.remaining_pecas[:]:
                aux += 1
                values = self.remove_possibilities(row, col)
                if values == 1 and (row, col) not in hi:
                    hi += ((row, col),)
                    break
            if lenght == aux:
                break
        #print(self.possible_moves)
        #print("\n")
        #print(self.remaining_pecas)
        #self.breakpoint()
        return self
   
    def acceptable_up_connections(self, row, col):
        if self.possible_moves[(row,col)] != () and self.possible_moves[(row,col)][0] == "0":
            move = self.possible_moves[(row,col)][1:]
            if move == "F":
                return ("BC", "BB", "VB", "LH", "VD", "BD")
            return ("FB", "BB", "BE", "BD", "VB", "VE", "LV")

        move = self.get_value(row, col)
        if move == "F":
            return ("BC", "BB", "VB", "LH", "VD", "BD")
        return ("FB", "BB", "BE", "BD", "VB", "VE", "LV")

    def acceptable_down_connections(self, row, col):
        if self.possible_moves[(row,col)] != () and self.possible_moves[(row,col)][0] == "0":
            move = self.possible_moves[(row,col)][1:]
            if move == "F":
                return ("BC", "BE", "BD", "VC", "VD", "LV")
            return ("FC", "BC", "BE", "BD", "VC", "VD", "LV")

        move = self.get_value(row, col)
        if move == "F":
            return ("BC", "BE", "BD", "VC", "VD", "LV")
        return ("FC", "BC", "BE", "BD", "VC", "VD", "LV")
    
    def acceptable_left_connections(self, row, col):
        if self.possible_moves[(row,col)] != () and self.possible_moves[(row,col)][0] == "0":
            move = self.possible_moves[(row,col)][1:]
            if move == "F":
                return ("BC", "BB", "BD", "VB", "VD", "LH")
            return ("FD", "BC", "BD", "BB", "VB", "VD", "LH")

        move = self.get_value(row, col)
        if move == "F":
            return ("BC", "BB", "BD", "VB", "VD", "LH")
        return ("FD", "BC", "BD", "BB", "VB", "VD", "LH")
    
    def acceptable_right_connections(self, row, col):
        if self.possible_moves[(row,col)] != () and  self.possible_moves[(row,col)][0] == "0":
            move = self.possible_moves[(row,col)][1:]
            if move == "F":
                return ("BC", "BB", "BE", "VC", "VE", "LH")
            return ("FE", "BC", "BE", "BB","VC", "VE", "LH")
        
        move = self.get_value(row, col)
        if move == "F":
            return ("BC", "BB", "BE", "VC", "VE", "LH")
        return ("FE", "BC", "BE", "BB","VC", "VE", "LH")
    
    def has_open_down_pipe(self, row, col):
        if self.possible_moves[(row,col)] != () and self.possible_moves[(row,col)][0] == "0":
            move = self.possible_moves[(row,col)][1:]
            if move in ("FB", "BB", "BE", "BD", "VB", "VE", "LV"):
                return 1
            return 0
        move = self.get_value(row, col)
        if move in ("FB", "BB", "BE", "BD", "VB", "VE", "LV"):
            return 1
        return 0
    
    def has_open_up_pipe(self, row, col):
        if self.possible_moves[(row,col)] != () and self.possible_moves[(row,col)][0] == "0":
            move = self.possible_moves[(row,col)][1:]
            if move in ("FC", "BC", "BE", "BD", "VC", "VD", "LV"):
                return 1
            return 0
        move = self.get_value(row, col)
        if move in ("FC", "BC", "BE", "BD", "VC", "VD", "LV"):
            return 1
        return 0
    
    def has_open_left_pipe(self, row, col):
        if self.possible_moves[(row,col)] != () and self.possible_moves[(row,col)][0] == "0":
            move = self.possible_moves[(row,col)][1:]
            if move in ("FE", "BC", "BE", "BB", "VC", "VE", "LH"):
                return 1
            return 0
        move = self.get_value(row, col)
        if move in ("FE", "BC", "BE", "BB", "VC", "VE", "LH"):
            return 1
        return 0

    def has_open_right_pipe(self, row, col):
        if self.possible_moves[(row,col)] != () and self.possible_moves[(row,col)][0] == "0":
            move = self.possible_moves[(row,col)][1:]
            if move in ("FD", "BC", "BD", "BB", "VB", "VD", "LH"):
                return 1
            return 0
        move = self.get_value(row, col)
        if move in ("FD", "BC", "BD", "BB", "VB", "VD", "LH"):
            return 1
        return 0

    def remove_possibilities(self, row, col):

        possibilities = ()

        if row != 0 and (self.possible_moves[(row - 1, col)] == () or self.possible_moves[(row - 1, col)][0] == "0") :
            cant_be_possibility = ()
            limits = self.check_frontiers(row, col)
            if self.has_open_down_pipe(row - 1,col):
                for connection in self.acceptable_down_connections(row - 1, col):
                    if self.get_value(row, col)[0] in connection and connection in limits:
                        possibilities += (connection,)
            else:
                if self.get_value(row - 1,col)[0] == "F" and self.get_value(row, col)[0] == "F":
                    cant_be_possibility = "FC"
                else:
                    for connection in self.acceptable_down_connections(row - 1, col):
                        if self.get_value(row, col)[0] in connection:
                            cant_be_possibility += (connection,)
                for possibility in self.get_all_possibilities(row, col):
                    if possibility not in cant_be_possibility and possibility in limits:
                        possibilities += (possibility,)

        if row != self.size - 1 and (self.possible_moves[(row + 1, col)] == () or self.possible_moves[(row + 1, col)][0] == "0") :
            cant_be_possibility = ()
            possibilities_aux = ()
            limits = self.check_frontiers(row, col)
            if self.has_open_up_pipe(row + 1,col):
                for connection in self.acceptable_up_connections(row + 1, col):
                    if self.get_value(row, col)[0] in connection and connection in limits:
                        possibilities_aux += (connection,)
            else:
                if self.get_value(row + 1,col)[0] == "F" and self.get_value(row, col)[0] == "F":
                    cant_be_possibility = "FB"
                else:
                    for connection in self.acceptable_up_connections(row + 1, col):
                        if self.get_value(row, col)[0] in connection:
                            cant_be_possibility += (connection,)
                for possibility in self.get_all_possibilities(row, col):
                    if possibility not in cant_be_possibility and possibility in limits:
                        possibilities_aux += (possibility,)
            if possibilities != ():
                possibilities = tuple(filter(lambda x: x in possibilities_aux, possibilities))
            else:
                possibilities = possibilities_aux

        if col != self.size - 1 and (self.possible_moves[(row, col + 1)] == () or self.possible_moves[(row, col + 1)][0] == "0"):
            possibilities_aux = ()
            cant_be_possibility = ()
            limits = self.check_frontiers(row, col)

            if self.has_open_left_pipe(row, col + 1):
                move = self.get_value(row,col)
                for connection in self.acceptable_left_connections(row, col + 1):
                    if self.get_value(row,col)[0] in connection and connection in limits:
                        possibilities_aux += (connection,)
            else:
                if self.get_value(row, col + 1)[0] == "F" and self.get_value(row, col)[0] == "F":
                    cant_be_possibility = "FD"
                else:
                    for connection in self.acceptable_left_connections(row, col + 1):
                        if self.get_value(row, col)[0] in connection:
                            cant_be_possibility += (connection,)
                for possibility in self.get_all_possibilities(row, col):
                    if possibility not in cant_be_possibility and possibility in limits:
                        possibilities_aux += (possibility,)
            if possibilities != ():
                possibilities = tuple(filter(lambda x: x in possibilities_aux, possibilities))
            else:
                possibilities = possibilities_aux

        if col != 0 and (self.possible_moves[(row, col - 1)] == () or self.possible_moves[(row, col - 1)][0] == "0"):
            possibilities_aux = ()
            cant_be_possibility = ()
            limits = self.check_frontiers(row, col)
            if self.has_open_right_pipe(row, col - 1):
                for connection in self.acceptable_right_connections(row, col - 1):
                    if self.get_value(row, col)[0] in connection and connection in limits:
                        possibilities_aux += (connection,)
            else:
                if self.get_value(row, col - 1)[0] == "F" and self.get_value(row, col)[0] == "F":
                    cant_be_possibility = "FE"
                else:
                    for connection in self.acceptable_right_connections(row, col - 1):
                        if self.get_value(row, col)[0] in connection:
                            cant_be_possibility += (connection,)
                for possibility in self.get_all_possibilities(row, col):
                    if possibility not in cant_be_possibility and possibility in limits:
                        possibilities_aux += (possibility,)
            if possibilities != ():
                possibilities = tuple(filter(lambda x: x in possibilities_aux, possibilities))
            else:
                possibilities = possibilities_aux

        if len(possibilities) == 1:
            old_possibilities = len(self.possible_moves[(row, col)])
            self.possible_moves[(row, col)] = "0" + possibilities[0]
            self.remaining_pecas.remove((row, col))
            self.remaining_pecas.insert(0, (row, col))
            self.count_actions -= old_possibilities - 1
            return 1
            """
            self.remaining_pecas.remove((row, col))
            self.set_cell(row, col, possibilities[0])
            """

        else:
            if possibilities:
                old_possibilities = self.possible_moves[(row, col)]
                self.possible_moves[(row, col)] = possibilities
                len_new_possibilities = len(possibilities)
                len_old_possibilities = len(old_possibilities)
                if len_old_possibilities != len_new_possibilities:
                    self.count_actions -= len_old_possibilities - len_new_possibilities
                    self.remaining_pecas.remove((row, col))
                    pos_to_insert = bisect.bisect_right([len(self.possible_moves[pos]) for pos in self.remaining_pecas], len_new_possibilities)
                    self.remaining_pecas.insert(pos_to_insert, (row, col))
                return 0
            """
            else: 
                abort
            """


    def set_cell(self, row, col, position):
        self.matrix[row][col] = position
    
    def get_all_possibilities(self, row, col):
        move = self.get_value(row, col)
        if move[0] == "F":
            return ("FC","FB", "FE", "FD")
        if move[0] == "B":
            return ("BC","BB", "BE", "BD")
        if move[0] == "V":
            return ("VC","VB", "VE", "VD")
        if move[0] == "L":
            return ("LH", "LV")
      
    def check_frontiers(self, row, col):

        move = self.matrix[row][col]
        if (col == 0 and (row == 0 or row == self.size - 1)) or (col == self.size - 1 and (row == 0 or row == self.size - 1)):
            if self.matrix[row][col][0] == "B" or self.matrix[row][col][0] == "L":
                self.invalid = True
                return ""
            if row == 0 and col == 0:
                if move[0] == "F":
                    return ("FD","FB")
                if move[0] == "V":
                    return ("VB",)
            elif row == 0 and col == self.size - 1:
                if move[0] == "F":
                    return ("FB","FE")
                if move[0] == "V":
                    return ("VE",)
            elif row == self.size - 1 and col == 0:
                if move[0] == "F":
                    return ("FC","FD")
                if move[0] == "V":
                    return ("VD",)
            elif row == self.size - 1 and col == self.size - 1:
                if move[0] == "F":
                    return ("FC","FE")
                if move[0] == "V":
                    return ("VC",)
        elif col == 0:
            if move[0] == "F":
                return ("FB","FC","FD")
            elif move[0] == "V":
                return ("VB","VD")
            elif move[0] == "L":
                return ("LV",)
            elif move[0] == "B":
                return ("BD",)
        elif col == self.size - 1:
            if move[0] == "F":
                return ("FB","FC","FE")
            elif move[0] == "V":
                return ("VC","VE")
            elif move[0] == "L":
                return ("LV",)
            elif move[0] == "B":
                return ("BE",)
        elif row == 0:
            if move[0] == "F":
                return ("FB","FE","FD")
            elif move[0] == "V":
                return ("VB","VE")
            elif move[0] == "L":
                return ("LH",)
            elif move[0] == "B":
                return ("BB",)
        elif row == self.size - 1:
            if move[0] == "F":
                return ("FC","FE","FD")
            elif move[0] == "V":
                return ("VC","VD")
            elif move[0] == "L":
                return ("LH",)
            elif move[0] == "B":
                return ("BC",)
        else:
            return self.get_all_possibilities(row, col)

    
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

    def get_next_peca(self):
        return self.remaining_pecas[0]
    
    def get_possibilities_for_peca(self, row, col):
        return self.possible_moves[(row, col)]

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
        partir do estado passado como argumento."""
        if state.board.invalid or state.board.get_remaining_pecas_count() == 0:
            return []

        row, col = state.board.get_next_peca()

        possibilities = state.board.get_possibilities_for_peca(row, col)
        if type(possibilities) == str:
            return [(row, col, possibilities)]
        return map(lambda peca: (row, col, peca), possibilities)
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state).
        (row, col, value) = action
        return PipeManiaState(state.board.set_number(row, col, value))"""
        (row, col, peca) = action
        return PipeManiaState(state.board.rodar_peça(row, col, peca))

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return state.board.get_remaining_pecas_count() == 0

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*.
        """
        board = node.state.board
        return board.count_actions
        pass


if __name__ == "__main__":
    board = Board.parse_instance()
    takuzu = PipeMania(board)
    goal_node = greedy_search(takuzu)
    print(goal_node.state.board.print(), sep="")
    pass
    
