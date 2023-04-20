import argparse
import copy
import sys
import time

cache = {}


class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):

        self.board = board
        self.width = 8
        self.height = 8
        self.parent = None
        self.eval = 0
        self.is_terminal = False

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

    def evl(self):
        return self.eval

    def evaluation(self, curr_turn: str):
        """
        """

        eval = 0
        num_moves_red = 0
        num_moves_black = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 'r':
                    eval += 1
                    if i != 0 and j != 0 and i != 7 and j != 7:
                        if get_next_turn(curr_turn) == 'b':
                            danger = in_danger(self, curr_turn, (i, j))
                            if danger:
                                eval -= 3
                    if 2 < i < 5:
                        eval += 0.5
                    elif i == 1:
                        eval += 0.5
                    if i != 0 and j != 0:
                        if self.board[i - 1][j - 1] == '.':
                            num_moves_red += 1
                    if i != 0 and j != 7:
                        if self.board[i - 1][j + 1] == '.':
                            num_moves_red += 1


                elif self.board[i][j] == 'R':
                    eval += 2
                    if i != 0 and j != 0 and i != 7 and j != 7:
                        if get_next_turn(curr_turn) == 'b':
                            danger = in_danger(self, curr_turn, (i, j))
                            if danger:
                                eval -= 6
                    if 2 < i < 5:
                        eval += 1
                    if i != 0 and j != 0:
                        if self.board[i - 1][j - 1] == '.':
                            num_moves_red += 1
                    if i != 0 and j != 7:
                        if self.board[i - 1][j + 1] == '.':
                            num_moves_red += 1
                    if i != 7 and j != 0:
                        if self.board[i + 1][j - 1] == '.':
                            num_moves_red += 1
                    if i != 7 and j != 7:
                        if self.board[i + 1][j + 1] == '.':
                            num_moves_red += 1


                elif self.board[i][j] == 'b':
                    eval -= 1
                    if i != 0 and j != 0 and i != 7 and j != 7:
                        if get_next_turn(curr_turn) == 'r':
                            danger = in_danger(self, curr_turn, (i, j))
                            if danger:
                                eval += 3
                    if 2 < i < 5:
                        eval -= 0.5
                    elif i == 6:
                        eval -= 0.5
                    if i != 7 and j != 0:
                        if self.board[i + 1][j - 1] == '.':
                            num_moves_black += 1
                    if i != 7 and j != 7:
                        if self.board[i + 1][j + 1] == '.':
                            num_moves_black += 1

                elif self.board[i][j] == 'B':
                    eval -= 2
                    if i != 0 and j != 0 and i != 7 and j != 7:
                        if get_next_turn(curr_turn) == 'r':
                            danger = in_danger(self, curr_turn, (i, j))
                            if danger:
                                eval += 6
                    if 2 < i < 5:
                        eval -= 1
                    if i != 0 and j != 0:
                        if self.board[i - 1][j - 1] == '.':
                            num_moves_black += 1
                    if i != 0 and j != 7:
                        if self.board[i - 1][j + 1] == '.':
                            num_moves_black += 1
                    if i != 7 and j != 0:
                        if self.board[i + 1][j - 1] == '.':
                            num_moves_black += 1
                    if i != 7 and j != 7:
                        if self.board[i + 1][j + 1] == '.':
                            num_moves_black += 1

        moves = num_moves_red - num_moves_black

        self.eval = (eval + moves)


def state_danger(curr_state: State, curr_turn: str):
    """
    check if given piece is in danger
    """
    for x in range(curr_state.height):
        for y in range(curr_state.width):
            if x != 0 and y != 0 and x != 7 and y != 7:
                if curr_state.board[x][y] == 'r' and curr_turn == 'r':
                    if curr_state.board[x - 1][y - 1] == 'b' or curr_state.board[x - 1][y - 1] == 'B':
                        if curr_state.board[x + 1][y + 1] == '.':
                            return True, 'r'
                    if curr_state.board[x - 1][y + 1] == 'b' or curr_state.board[x - 1][y + 1] == 'B':
                        if curr_state.board[x + 1][y - 1] == '.':
                            return True, 'r'
                    if curr_state.board[x + 1][y - 1] == 'B' and curr_state.board[x - 1][y + 1] == '.':
                        return True, 'r'
                    if curr_state.board[x + 1][y + 1] == 'B' and curr_state.board[x - 1][y - 1] == '.':
                        return True, 'r'

                elif curr_state.board[x][y] == 'R' and curr_turn == 'r':
                    if curr_state.board[x - 1][y - 1] == 'b' or curr_state.board[x - 1][y - 1] == 'B':
                        if curr_state.board[x + 1][y + 1] == '.':
                            return True, 'R'
                    if curr_state.board[x - 1][y + 1] == 'b' or curr_state.board[x - 1][y + 1] == 'B':
                        if curr_state.board[x + 1][y - 1] == '.':
                            return True, 'R'
                    if curr_state.board[x + 1][y - 1] == 'B' and curr_state.board[x - 1][y + 1] == '.':
                        return True, 'R'
                    if curr_state.board[x + 1][y + 1] == 'B' and curr_state.board[x - 1][y - 1] == '.':
                        return True, 'R'

                elif curr_state.board[x][y] == 'b' and curr_turn == 'b':
                    if curr_state.board[x + 1][y - 1] == 'r' or curr_state.board[x + 1][y - 1] == 'R':
                        if curr_state.board[x - 1][y + 1] == '.':
                            return True, 'b'
                    if curr_state.board[x + 1][y + 1] == 'r' or curr_state.board[x + 1][y + 1] == 'R':
                        if curr_state.board[x - 1][y - 1] == '.':
                            return True, 'b'
                    if curr_state.board[x - 1][y + 1] == 'R' and curr_state.board[x + 1][y - 1] == '.':
                        return True, 'b'
                    if curr_state.board[x - 1][y - 1] == 'R' and curr_state.board[x + 1][y + 1] == '.':
                        return True, 'b'

                elif curr_state.board[x][y] == 'B' and curr_turn == 'b':
                    if curr_state.board[x + 1][y - 1] == 'r' or curr_state.board[x + 1][y - 1] == 'R':
                        if curr_state.board[x - 1][y + 1] == '.':
                            return True, 'B'
                    if curr_state.board[x + 1][y + 1] == 'r' or curr_state.board[x + 1][y + 1] == 'R':
                        if curr_state.board[x - 1][y - 1] == '.':
                            return True, 'B'
                    if curr_state.board[x - 1][y + 1] == 'R' and curr_state.board[x + 1][y - 1] == '.':
                        return True, 'B'
                    if curr_state.board[x - 1][y - 1] == 'R' and curr_state.board[x + 1][y + 1] == '.':
                        return True, 'B'

    return False, '.'


def in_danger(curr_state:State, curr_turn:str, coord_xy:(int, int)):
    """
    check if given piece is in danger
    """

    x, y = coord_xy

    if curr_state.board[x][y] == 'r' or curr_state.board[x][y] == 'R':
        if curr_state.board[x-1][y-1] == 'b' or curr_state.board[x-1][y-1] == 'B':
            if curr_state.board[x + 1][y + 1] == '.':
                return True
        if curr_state.board[x-1][y+1] == 'b' or curr_state.board[x-1][y+1] == 'B':
            if curr_state.board[x + 1][y - 1] == '.':
                return True
        if curr_state.board[x+1][y-1] == 'B' and curr_state.board[x-1][y+1] == '.':
            return True
        if curr_state.board[x+1][y+1] == 'B' and curr_state.board[x-1][y-1] == '.':
            return True

    elif curr_state.board[x][y] == 'b' or curr_state.board[x][y] == 'B':
        if curr_state.board[x+1][y-1] == 'r' or curr_state.board[x+1][y-1] == 'R':
            if curr_state.board[x - 1][y + 1] == '.':
                return True
        if curr_state.board[x+1][y+1] == 'r' or curr_state.board[x+1][y+1] == 'R':
            if curr_state.board[x - 1][y - 1] == '.':
                return True
        if curr_state.board[x-1][y+1] == 'R' and curr_state.board[x+1][y-1] == '.':
            return True
        if curr_state.board[x-1][y-1] == 'R' and curr_state.board[x+1][y+1] == '.':
            return True

    return False

def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']


def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'


def deep_copy(curr_state: State):
    """

    :param curr_state:
    :return:
    """
    new_board = [[None] * 8 for i in range(8)]
    new = State(new_board)
    x = 0
    for i in curr_state.board:
        y = 0
        for j in i:
            new.board[x][y] = j
            y += 1
        x += 1
    return new


def perform_move(curr_state: State, cord_xy: (int, int), new_xy: (int, int)):
    """

    :param curr_state:
    :param cord_xy:
    :param new_xy:
    :return:
    """
    new_state = deep_copy(curr_state)
    x, y = cord_xy
    new_x, new_y = new_xy
    if new_x == 7 and new_state.board[x][y] == 'b':
        new_state.board[new_x][new_y] = 'B'
        new_state.board[x][y] = '.'
    elif new_x == 0 and new_state.board[x][y] == 'r':
        new_state.board[new_x][new_y] = 'R'
        new_state.board[x][y] = '.'
    else:
        new_state.board[new_x][new_y] = new_state.board[x][y]
        new_state.board[x][y] = '.'

    return new_state


def perform_jump(curr_state: State, cord_xy: (int, int), jump_xy: (int, int), new_xy: (int, int)):
    """

    :param curr_state:
    :param cord_xy:
    :param new_xy:
    :return:
    """
    new_state = deep_copy(curr_state)
    x, y = cord_xy
    new_x, new_y = new_xy
    jump_x, jump_y = jump_xy
    if new_x == 7 and new_state.board[x][y] == 'b':
        new_state.board[new_x][new_y] = 'B'

    elif new_x == 0 and new_state.board[x][y] == 'r':
        new_state.board[new_x][new_y] = 'R'
    else:
        new_state.board[new_x][new_y] = new_state.board[x][y]
    new_state.board[x][y] = '.'
    new_state.board[jump_x][jump_y] = '.'
    return new_state


def check_jump(curr_state: State, curr_turn: str, cord_xy: (int, int), king: bool):
    """

    :param curr_state:
    :param curr_turn:
    :param cord_xy:
    :return:
    """

    opp, opp_king = get_opp_char(curr_turn)
    x, y = cord_xy
    jumped = None

        # first check if black can jump
    if curr_state.board[x][y] == curr_turn and curr_turn == 'b':
        if y != 0 and y != 1 and x != 7 and x != 6:
            if (curr_state.board[x + 1][y - 1] == opp or curr_state.board[x + 1][y - 1] == opp_king) and \
                    curr_state.board[x + 2][y - 2] == '.':
                #print("this black can JUMP left", x, y)
                jumped = perform_jump(curr_state, (x, y), (x + 1, y - 1), (x+2, y-2))
                second_jump = check_jump(jumped, curr_turn, (x+2, y-2), king)
                if second_jump is None:
                    return jumped
                else:
                    return second_jump

        if x != 7 and y != 7 and x != 6 and y != 6:
            if (curr_state.board[x + 1][y + 1] == opp or curr_state.board[x + 1][y + 1] == opp_king) and \
                    curr_state.board[x + 2][y + 2] == '.':
                #print("this black can JUMP right", x, y)
                jumped = perform_jump(curr_state, (x, y), (x + 1, y + 1), (x + 2, y + 2))
                second_jump = check_jump(jumped, curr_turn, (x + 2, y + 2), king)
                if second_jump is None:
                    return jumped
                else:
                    return second_jump
    # now check if red can jump
    if curr_state.board[x][y] == curr_turn and curr_turn == 'r':
        if x != 0 and x != 1 and y != 7 and y != 6:
            if (curr_state.board[x - 1][y + 1] == opp or curr_state.board[x - 1][y + 1] == opp_king) and \
                    curr_state.board[x - 2][y + 2] == '.':
                #print("this red can JUMP right", x, y)
                jumped = perform_jump(curr_state, (x, y), (x - 1, y + 1), (x - 2, y + 2))
                second_jump = check_jump(jumped, curr_turn, (x - 2, y + 2), king)
                if second_jump is None:
                    return jumped
                else:
                    return second_jump

        if x != 0 and x != 1 and y != 0 and y != 1:
            if (curr_state.board[x - 1][y - 1] == opp or curr_state.board[x - 1][y - 1] == opp_king) and \
                    curr_state.board[x - 2][y - 2] == '.':
                #print("this red can JUMP left", x, y)
                jumped = perform_jump(curr_state, (x, y), (x - 1, y - 1), (x - 2, y - 2))
                second_jump = check_jump(jumped, curr_turn, (x - 2, y - 2), king)
                if second_jump is None:
                    return jumped
                else:
                    return second_jump
    # check if king piece can jump

    if (curr_state.board[x][y] == 'B' and curr_turn == 'b') or (curr_state.board[x][y] == 'R' and curr_turn == 'r'):
        if y != 0 and y != 1 and x != 7 and x != 6:
            if (curr_state.board[x + 1][y - 1] == opp or curr_state.board[x + 1][y - 1] == opp_king) and \
                    curr_state.board[x + 2][y - 2] == '.':
                #print("this king can JUMP down left", x, y)
                jumped = perform_jump(curr_state, (x, y), (x + 1, y - 1), (x + 2, y - 2))
                second_jump = check_jump(jumped, curr_turn, (x + 2, y - 2), king)
                if second_jump is None:
                    return jumped
                else:
                    return second_jump
        if x != 7 and y != 7 and x != 6 and y != 6:
            if (curr_state.board[x + 1][y + 1] == opp or curr_state.board[x + 1][y + 1] == opp_king) and \
                    curr_state.board[x + 2][y + 2] == '.':
                #print("this king can JUMP down right", x, y)
                jumped = perform_jump(curr_state, (x, y), (x + 1, y + 1), (x + 2, y + 2))
                second_jump = check_jump(jumped, curr_turn, (x + 2, y + 2), king)
                if second_jump is None:
                    return jumped
                else:
                    return second_jump

        if x != 0 and x != 1 and y != 7 and y != 6:
            if (curr_state.board[x - 1][y + 1] == opp or curr_state.board[x - 1][y + 1] == opp_king) and \
                    curr_state.board[x - 2][y + 2] == '.':
                #print("this king can JUMP up right", x, y)
                jumped = perform_jump(curr_state, (x, y), (x - 1, y + 1), (x - 2, y + 2))
                second_jump = check_jump(jumped, curr_turn, (x - 2, y + 2), king)
                if second_jump is None:
                    return jumped
                else:
                    return second_jump

        if x != 0 and x != 1 and y != 0 and y != 1:
            if (curr_state.board[x - 1][y - 1] == opp or curr_state.board[x - 1][y - 1] == opp_king) and \
                    curr_state.board[x - 2][y - 2] == '.':
                #print("this king can JUMP up left", x, y)
                jumped = perform_jump(curr_state, (x, y), (x - 1, y - 1), (x - 2, y - 2))
                second_jump = check_jump(jumped, curr_turn, (x - 2, y - 2), king)
                if second_jump is None:
                    return jumped
                else:
                    return second_jump

    return None


def get_successors(curr_state: State, curr_turn: str):
    """

    :return:
    """
    successors = []
    x = 0
    for i in curr_state.board:
        y = 0
        for j in i:
            # moving black diagonally
            if j == curr_turn and curr_turn == 'b' and x != 7:
                # check if it can jump
                check = check_jump(curr_state, curr_turn, (x, y), False)
                if check:
                    # return only the one possible option
                    return [check]
                else:
                    if y != 0:
                        if curr_state.board[x + 1][y - 1] == '.':
                            # this black piece can move diagonally on left side
                            #print("this black will move left", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x + 1, y - 1)))
                    if y != 7:
                        if curr_state.board[x + 1][y + 1] == '.':
                            # this black piece can move diagonally on right side
                            #print("this black will move right", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x + 1, y + 1)))

            # moving red diagonally
            elif j == curr_turn and curr_turn == 'r' and x != 0:
                # check if it can jump
                check = check_jump(curr_state, curr_turn, (x, y), False)
                if check:
                    # return only the one possible option
                    return [check]
                else:
                    if y != 0:
                        if curr_state.board[x - 1][y - 1] == '.':
                            # this red piece can move diagonally on left side
                            #print("this red will move left", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x - 1, y - 1)))
                    if y != 7:
                        if curr_state.board[x - 1][y + 1] == '.':
                            # this black piece can move diagonally on right side
                            #print("this red will move right", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x - 1, y + 1)))

            # moving kings diagonally
            # move black king diagonally
            elif j == 'B' and curr_turn == 'b':
                check = check_jump(curr_state, curr_turn, (x, y), True)
                if check:
                    # return only the one possible option
                    return [check]
                else:
                    if y != 0 and x != 7:
                        if curr_state.board[x + 1][y - 1] == '.':
                            # this black piece can move diagonally on left side
                            #print("this black king will move down left", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x + 1, y - 1)))
                    if y != 0 and x != 0:
                        if curr_state.board[x - 1][y - 1] == '.':
                            # this black piece can move diagonally on left side
                            #print("this black king will move up left", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x - 1, y - 1)))
                    if y != 7 and x != 7:
                        if curr_state.board[x + 1][y + 1] == '.':
                            # this black piece can move diagonally on right side
                            #print("this black will king move down right", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x + 1, y + 1)))
                    if y != 7 and x != 0:
                        if curr_state.board[x - 1][y + 1] == '.':
                            # this black piece can move diagonally on left side
                            #print("this black king will move up right", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x - 1, y + 1)))

            # moving red king diagonally
            elif j == 'R' and curr_turn == 'r':
                check = check_jump(curr_state, curr_turn, (x, y), True)
                if check:
                    # return only the one possible option
                    return [check]
                else:
                    if y != 0 and x != 7:
                        if curr_state.board[x + 1][y - 1] == '.':
                            # this black piece can move diagonally on left side
                            #print("this red king will move down left", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x + 1, y - 1)))
                    if y != 0 and x != 0:
                        if curr_state.board[x - 1][y - 1] == '.':
                            # this black piece can move diagonally on left side
                            #print("this red king will move up left", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x - 1, y - 1)))
                    if y != 7 and x != 7:
                        if curr_state.board[x + 1][y + 1] == '.':
                            # this black piece can move diagonally on right side
                            #print("this red will king move down right", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x + 1, y + 1)))
                    if y != 7 and x != 0:
                        if curr_state.board[x - 1][y + 1] == '.':
                            # this black piece can move diagonally on left side
                            #print("this red king will move up right", x, y)
                            successors.append(perform_move(curr_state, (x, y), (x - 1, y + 1)))

            y += 1

        x += 1

    return successors


def node_ordering(successors:[], curr_turn:str, order:str):
    """

    """

    for successor in successors:
        successor.evaluation(curr_turn)

    if order == 'max':
        successors.sort(key=lambda x: x.evl(), reverse=True)
    else:
        successors.sort(key=lambda x: x.evl())

    return successors


def max_value(curr_state:State, alpha:float, beta:float, depth:int, curr_turn:str):
    """

    """
    str_state = curr_state.__str__() + curr_turn
    if str_state in cache.keys() and cache[str_state][2] >= depth:
        return cache[str_state][0], cache[str_state][1]
    if depth == 0:
        curr_state.evaluation(curr_turn)
        return curr_state.eval, None

    successors = get_successors(curr_state, curr_turn)
    if len(successors) == 0:
        cache[str_state] = (-1000000000, None, depth)
        return -1000000000, None

    #successors.sort(key=lambda x: x.evaluation(curr_turn), reverse=True)
    #successors = node_ordering(successors, curr_turn, 'max')
    v = float('-inf')
    move = curr_state
    for child in successors:
        temp_val, temp_state = min_value(child, alpha, beta, depth - 1, get_next_turn(curr_turn))
        if temp_val > v:
            v = temp_val
            move = child
        if temp_val > beta:
            cache[str_state] = (v, child, depth)
            return v, child
        alpha = max(alpha, temp_val)
    cache[str_state] = (v, move, depth)
    return v, move


def min_value(curr_state:State, alpha:float, beta:float, depth:int, curr_turn:str):
    """
    """
    str_state = curr_state.__str__() + curr_turn
    if str_state in cache.keys() and cache[str_state][2] >= depth:
        return cache[str_state][0], cache[str_state][1]
    if depth == 0:
        curr_state.evaluation(curr_turn)
        return curr_state.eval, None

    successors = get_successors(curr_state, curr_turn)
    if len(successors) == 0:
        cache[str_state] = (1000000000, None, depth)
        return 1000000000, None

    #successors.sort(key=lambda state:state.evaluation(curr_turn))
    #successors = node_ordering(successors, curr_turn, 'min')
    v = float('inf')
    move = curr_state
    for child in successors:
        temp_val, temp_state = max_value(child, alpha, beta, depth - 1, get_next_turn(curr_turn))
        if temp_val < v:
            v = temp_val
            move = child
        if temp_val < alpha:
            cache[str_state] = (v, child, depth)
            return v, child
        beta = min(beta, temp_val)
    cache[str_state] = (v, move, depth)
    return v, move


def alpha_beta_search_red(curr_state: State, depth: int, curr_turn:str):
    v, move = max_value(curr_state, float('-inf'), float('inf'), depth, curr_turn)
    return move


def alpha_beta_search_black(curr_state: State, depth: int, curr_turn:str):
    v, move = min_value(curr_state, float('-inf'), float('inf'), depth, curr_turn )
    return move


def run_game(state: State, curr_turn: str):
    """

    """

    while state.eval != 1000000000 and state.eval != -1000000000:
        state.display()
        if curr_turn == 'r':
            next_red = alpha_beta_search_red(state, 10, curr_turn)
            if next_red is not None:
                next_red.parent = state
                state = next_red
            else:
                break
        else:
            next_black = alpha_beta_search_black(state, 10, curr_turn)
            if next_black is not None:
                next_black.parent = state
                state = next_black
            else:
                break
        curr_turn = get_next_turn(curr_turn)
    return state


def print_output(output_file: str, final_state: State, initial_state:State):
    """
    function to print the final output of all the states starting from initial to final in a text file.
    """

    states = [final_state]
    parent = final_state.parent
    states.append(parent)
    while parent != initial_state:
        if parent.parent is not None:
            states.append(parent.parent)
            parent = parent.parent
        else:
            break

    f = open(output_file, "w")
    print(len(states))
    for child in reversed(states):
        for row in child.board:
            for ch in row:
                f.write(ch)
            f.write("\n")
        f.write("\n")
    f.close()


def read_from_file(filename):
    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()
    return board


def get_maxDepth(curr_state:State):
    """

    :param curr_state:
    :return:
    """
    count = 0
    for i in curr_state.board:
        for j in i:
            if j == 'r' or j == 'b':
                count += 1
    return count

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    in_state = State(initial_board)
    max_depth = get_maxDepth(in_state)
    turn = 'r'
    ctr = 0
    final_state = run_game(in_state, turn)
    print_output(args.outputfile, final_state, in_state)
    print(max_depth)
