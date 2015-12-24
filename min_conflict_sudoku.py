import random, copy

class SudokuMinConflict:

    def __init__(self, N, M, K, board):
        '''
        Initializes the board and N,M,K values
        :param N: size of board
        :param M: size of row of grid
        :param K: size of column of grid
        :param board: board state
        :return:
        '''
        self.size = N
        self.M = M
        self.K = K
        self.board = board

        self.fixed_positions = []
        self.non_fixed_pos = []
        self.domain_values = {}

        self.grid = lambda pos: (int(pos[0]/self.M), int(pos[1]/self.K))

        for x in range(self.size):
            for y in range(self.size):
                pos = (x, y)
                if board[x][y] != 0:
                    self.fixed_positions.append(pos)
                else:
                    self.non_fixed_pos.append(pos)
                    self.domain_values[pos] = [i for i in range(1, self.size+1)]

    def initialize_random_start_state(self):

        '''
        Initialize the given board state with random values
        :return: new board state
        '''
        for x in range(self.size):
            for y in range(self.size):
                pos = (x, y)
                if pos not in self.fixed_positions:
                    # Remove unwanted values from domain
                    self.domain_values[pos] = self.apply_constraint(pos)
                    self.board[x][y] = random.choice(self.domain_values[pos])

        return self.board

    def apply_constraint(self, pos):

        '''
        Removes that value from the domain of this position - row or column or grid
        :param position: The position for which we need to update domain
        :return: New domain for this position
        '''
        new_domain = self.domain_values[pos]
        x, y = pos

        for fixed_x, fixed_y in self.fixed_positions:
            if fixed_x == x or fixed_y == y or \
                self.grid((fixed_x,fixed_y)) == self.grid(pos):

                val = self.board[fixed_x][fixed_y]
                try: new_domain.remove(val)
                except: pass

        return new_domain

    def get_random_con_var(self, board):
        '''
        Returns a randomly selected conflicted variable
        :param board:
        :return:
        '''
        all_pos_list = copy.deepcopy(self.non_fixed_pos)

        while all_pos_list:

            pos = random.choice(all_pos_list)
            if self.number_of_conflicts(board, pos) > 0:
                return pos
            else:
                all_pos_list.remove(pos)

        return -1

    def number_of_conflicts(self, board, pos):
        '''
        Calculates and returns number of conflicts in this board with respect
        to this position
        :param board:
        :param position:
        :return:
        '''
        x,y = pos
        val = board[x][y]
        count = 0

        for i in range(self.size):
            if (i != y) and (board[x][i] == val):
                count = count + 1

        for i in range(self.size):
            if (i != x) and (board[i][y] == val):
                count = count + 1

        grid = self.grid(pos)
        gridX = grid[0]*self.M, grid[1]*self.K
        gridY = gridX[0]+self.M, gridX[1]+self.K

        for i in range(gridX[0],gridY[0]):
            for j in range(gridX[1],gridY[1]):
                if ((i,j) != pos) and (board[i][j] == val):
                    count = count + 1

        return count
    
    def get_least_con_val(self, board, var):
        '''
        Find the least conflicted value for variable var
        :param board:
        :param var:
        :return:
        '''
        conflicts = {}

        # For all possible values of conflict variable,
        # find the number of conflicts it gives.
        for val in self.domain_values[var]:
            new_state = self.update_board(board, var, val)
            conflicts[val] = self.number_of_conflicts(new_state, var)

        min_conflict_val = sorted(conflicts.values())[0]

        # If more than one minimum break ties randomly
        all_min_values = [k for k, v in conflicts.items() if v == min_conflict_val]

        min_val = random.choice(all_min_values)
        return min_val

    def update_board(self, board, var, val):
        x,y = var
        board[x][y] = val
        return board