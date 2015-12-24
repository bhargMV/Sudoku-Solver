###########################################
# you need to implement five funcitons here
###########################################
import re
import copy
from min_conflict_sudoku import SudokuMinConflict
import random
import copy

board = []
N = 0
M = 0
K = 0
temp_board = []
legal_value = []
count = 0

def readFile(filename):
    '''

    :param filename: reads from the file and generate the puzzle board
    :return: puzzle board
    '''

    f = open(filename)
    line1 = f.readline()

    line1_c = [x.strip() for x in line1.replace(';','').split(',')]


    global N
    N = int(line1_c[0])

    global M
    M = int(line1_c[1])

    global K
    K = int(line1_c[2])

    global board
    board = []

    for i in range(0, N):
        line = f.readline()
        line_c = []

        for x in line.replace(';','').split(','):
            if x.strip() == '-':
                line_c.append(0)

            else:
                line_c.append(int(x.strip()))


        board.append(line_c)

    return board


def initializeLegalValues():
    '''
    Initializes remaining legal values for all the cells in the puzzle board
    :return:
    '''
    temp_list = []
    for k in range(1, N+1):
        temp_list.append(k)

    global legal_value
    legal_value = []

    for i in range(0, N):
        legal_value.append([])
        for j in range(0, N):
            legal_value[i].append([])
            legal_value[i][j] = copy.deepcopy(temp_list)


def FindUnassignedLocation(board):
    '''
    :param board: Puzzle board
    :return: an unfilled cell
    '''
    for row in range(0,N):
        for col in range(0,N):
            if (board[row][col] == 0):
                return [row, col]
    return [-1, -1]


def findMostConstrained(board):
    '''
    :param board: Puzzle board
    :return: Most constrained Cell
    '''
    min_X = -1
    min_Y = -1
    min_count = N + 1

    #print legal_value

    for row in range(0,N):
        for col in range(0,N):
            global legal_value

            if board[row][col] == 0 and len(legal_value[row][col]) == 0:
                return[-2,-2]

            if board[row][col] == 0 and len(legal_value[row][col]) < min_count:
                min_X = row
                min_Y = col
                min_count = len(legal_value[row][col])

    return [min_X, min_Y]



def removeLegalValues(board, row, col, num):
    '''
    :param board:  Puzzle board
    :param row: row number
    :param col: column number
    :param num: value to be removed from legal value list of corresponding cell
    :return: Nothing
    '''

    global legal_value

    for c in range(0,N):
        if board[row][c] == 0 and num in legal_value[row][c]:
            (legal_value[row][c]).remove(num)

    for r in range(0,N):
        if board[r][col] == 0 and num in legal_value[r][col]:
            (legal_value[r][col]).remove(num)

    temp_r = row - row%M
    temp_c = col - col%K

    for r in range(0,M):
         for c in range(0,K):
             if board[temp_r + r][temp_c + c] == 0 and num in legal_value[temp_r + r][temp_c + c]:
                (legal_value[temp_r + r][temp_c + c]).remove(num)


def addLegalValues(board, row, col, num, temp_leg):
    """
    :param board:  Puzzle board
    :param row: row number
    :param col: column number
    :param num: value to be added to legal value list of corresponding cell
    :return: Nothing
    """

    global legal_value

    for c in range(0,N):
        if board[row][c] == 0 and num not in legal_value[row][c] and num in temp_leg[row][c]:
            (legal_value[row][c]).append(num)

    for r in range(0,N):
        if board[r][col] == 0 and num not in legal_value[r][col] and num in temp_leg[r][col]:
            (legal_value[r][col]).append(num)

    temp_r = row - row%M
    temp_c = col - col%K

    for r in range(0,M):
         for c in range(0,K):
             if board[temp_r + r][temp_c + c] == 0 and num not in legal_value[temp_r + r][temp_c + c] and num in temp_leg[temp_r + r][temp_c + c]:
                (legal_value[temp_r + r][temp_c + c]).append(num)



def anyZeroLegalValues(board, row, col, num):
    '''
    :param board:  Puzzle board
    :param row: row number
    :param col: column number
    :param num: Check if num is the only legal value for the cell
    :return: Nothing
    '''

    global legal_value
    for c in range(0,N):
        if c == col:
            continue

        if board[row][c] == 0 and len(legal_value[row][c]) == 1 and (num in legal_value[row][c]):
            return 1

    for r in range(0,N):
        if r == row:
            continue

        if board[r][col] == 0 and len(legal_value[r][col]) == 1 and (num in legal_value[r][col]):
            return 1

    temp_r = row - row%M
    temp_c = col - col%K

    for r in range(0,M):
         for c in range(0,K):

             if temp_r + r == row and temp_c + c == col:
                 continue

             if board[temp_r + r][temp_c + c] == 0 and len(legal_value[temp_r + r][temp_c + c]) == 1 and (num in legal_value[temp_r + r][temp_c + c]):
                return 1
    return 0


def isSafe(board, row, col, num):
    '''
    Checks if puzzle board is valid after inserting num in particular cell
    :param board: puzzle board
    :param row: row number
    :param col: column number
    :param num:
    :return: true or false
    '''
    for c in range(0,N):
        if (board[row][c] == num):
            return 0

    for r in range(0,N):
        if (board[r][col] == num):
            return 0

    temp_r = row - row%M
    temp_c = col - col%K

    for r in range(0,M):
         for c in range(0,K):
            if (board[temp_r + r][temp_c + c] == num):
                return 0

    return 1


def arc_consistent(board, row, col):
    '''
    Checks for arc consistency for this particular cell of the board
    and recursively for the whole board
    :param board:
    :param row:
    :param col:
    :return:
    '''
    if forwardCheck(board, row, col) == False:
        return False

    for i in range(0,N):

        if board[row][i] == 0 and forwardCheck(board, row, i) == False:
            return False

        if board[i][col] == 0 and forwardCheck(board, i, col) == False:
            return False

    return True

def forwardCheck(board,row,col):
    '''
    Checks if any legal values are violated.
    Forward checks
    :param board:
    :param row:
    :param col:
    :return:
    '''
    global legal_value
    for i in range(0, N):

        if board[row][i] == 0:
            if len(legal_value[row][i]) == 0:
                return False

        if board[i][col] == 0:
            if len(legal_value[i][col]) == 0:
                return False

    return True



def backTrackingUtil(board):
    '''
    Implementation of simple Backtracking Algorithm
    :param board: Input board
    :return: Solved Puzzle board and consistency checks
    '''
    pos = FindUnassignedLocation(board)

    if(pos[0] == -1):
        return 1

    row = pos[0]
    col = pos[1]


    for num in range(1, N+1):

        if (isSafe(board, row, col, num)):
            board[row][col] = num

            global count
            count = count + 1
            if (backTrackingUtil(board)):
                return 1

            board[row][col] = 0

    return 0



def backTrackingMRVUtil(board):
    '''
    Implementation of Backtracking Algorithm using MRV Heuristic
    :param board: Input board
    :return: Solved Puzzle board and consistency checks
    '''

    pos = findMostConstrained(board)

    if(pos[0] == -1):
        return 1

    if(pos[0] == -2):
        return 0

    row = pos[0]
    col = pos[1]


    for num in range(1, N+1):

        global legal_value
        ##Check for only legal values
        if(num in legal_value[row][col]):
        #if (isSafe(board, row, col, num)):

            board[row][col] = num

            temp_leg = copy.deepcopy(legal_value)

            removeLegalValues(board, row, col, num)

            global count
            count = count + 1
            if (backTrackingMRVUtil(board)):
                return 1

            addLegalValues(board, row, col, num, temp_leg)

            board[row][col] = 0


            del temp_leg

    return 0



def backTrackingMRVFwdUtil(board):
    '''
    Implementation of Backtracking Algorithm using MRV Heuristic and forward checking
    :param board: Input board
    :return: Solved Puzzle board and consistency checks
    '''

    pos = findMostConstrained(board)

    if(pos[0] == -1):
        return 1

    if(pos[0] == -2):
        return 0

    row = pos[0]
    col = pos[1]


    for num in range(1, N+1):

        ##Check for only legal values
        global legal_value
        if(num in legal_value[row][col]):
        #if (isSafe(board, row, col, num)):

            board[row][col] = num


            if(anyZeroLegalValues(board, row,col,num)):
                board[row][col] = 0
                continue


            temp_leg = copy.deepcopy(legal_value)

            removeLegalValues(board, row, col, num)

            global count
            count = count + 1
            if (backTrackingMRVFwdUtil(board)):
                return 1

            addLegalValues(board, row, col, num, temp_leg)
            board[row][col] = 0


            del temp_leg

    return 0



def backtrackingMRVcpUtil(board):
    '''
    Implementation of Backtracking Algorithm using MRV Heuristic and Constraint Propagation
    :param board: Input board
    :return: Solved Puzzle board and consistency checks
    '''

    global count
    x,y = FindUnassignedLocation(board)
    if (-1,-1) == (x,y):
        return True

    x,y = findMostConstrained(board)
    if (-2,-2) == (x,y):
        return False

    # Check legal_values
    #print "cell(", x,y, ")has legal values = ", legal_value[x][y]

    for i in range (1,N+1):
        # Try assigning all possible to this cell
        if i in legal_value[x][y]:
            board[x][y] = i
            temp_leg = copy.deepcopy(legal_value)
            removeLegalValues(board, x,y,i)

            # Check for arc consistency
            if (arc_consistent(board, x,y) == False):
                addLegalValues(board, x, y, i, temp_leg)
                board[x][y] = 0
                continue

            count = count + 1

            if backtrackingMRVcpUtil(board):
                return True

            addLegalValues(board, x, y, i, temp_leg)
            board[x][y] = 0

    return False


##############################################################################
##############################################################################

def backtracking(filename):
    ###
    # use backtracking to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    readFile(str(filename))

    global count
    count = 0

    global temp_board, board
    temp_board = []
    temp_board = copy.deepcopy(board)

    if backTrackingUtil(temp_board):
        #print board
        return (temp_board, count)

    temp_board = []
    board = []

    return ([[],[]], count)





def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    readFile(str(filename))

    global temp_board, board
    temp_board = []
    temp_board = copy.deepcopy(board)

    initializeLegalValues()

    for r in range(0, N):
        for c in range(0, N):
            if(temp_board[r][c] != 0):
                removeLegalValues(temp_board, r, c, temp_board[r][c])

    global count
    count = 0
    if backTrackingMRVUtil(temp_board):
        #print board

        #for r in range(0, len(temp_board)):
            #print temp_board[r]

        return (temp_board, count)

    temp_board = []
    board = []

    return ([[],[]], count)



def backtrackingMRVfwd(filename):
    ###
    # use backtracking +MRV + forward propogation
    # to solve sudoku puzzle here,
    # return the solution in the form of list of 
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    
    readFile(str(filename))

    global temp_board, board
    temp_board = []
    temp_board = copy.deepcopy(board)

    initializeLegalValues()

    for r in range(0, N):
        for c in range(0, N):
            if(temp_board[r][c] != 0):
                removeLegalValues(temp_board, r, c, temp_board[r][c])

    global count
    count = 0
    if backTrackingMRVFwdUtil(temp_board):
        #print board
        #for r in range(0, len(temp_board)):
            #print temp_board[r]

        return (temp_board, count)


    temp_board = []
    board = []

    return [[],[]], count



def backtrackingMRVcp(filename):
    '''
    Uses backtracking + MRV + cp
    :param filename: Input game state file
    :return: Final game state, consistency check count
    '''

    initial_board = readFile(filename)
    global count
    count = 0
    temp_board = copy.deepcopy(initial_board)


    initializeLegalValues()

    for r in range(0, N):
        for c in range(0, N):
            if(temp_board[r][c] != 0):
                removeLegalValues(temp_board, r, c, temp_board[r][c])

    if backtrackingMRVcpUtil(temp_board):
        #for r in range(0, len(temp_board)):
            #print temp_board[r]
        return (temp_board, count)

    return ([[],[]], 0)


def minConflict(filename):
    '''
    Uses minConflict to solve sudoku puzzle.
    :param filename: Input game state file
    :return: Final game state, consistency check count
    '''

    initial_board = readFile(filename)

    instance = SudokuMinConflict(N,M,K,initial_board)
    iterations = 500000
    state = instance.initialize_random_start_state()
    prev_state = copy.deepcopy(state)

    for i in range(iterations):
        var = instance.get_random_con_var(state)
        if var == -1:
            return (state, i)

        val = instance.get_least_con_val(state, var)
        state = instance.update_board(state, var, val)

        # Break the local Minima problem
        # When the same state is repeated for 8 times, introduce more
        # conflicts by randomly assinging a value to variable
        if i%8 == 0:
            if prev_state == state:
                state = instance.update_board(state, var, random.randint(1,N))
            prev_state = copy.deepcopy(state)

    return ([[],[]], 0)