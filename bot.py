from copy import *

EMPTY_PLACE_SCORE = 200
EMPTY_CORNER_SCORE = 100
WIN_SCORE = 1000
LOSE_SCORE = -1000
DRAW_SCORE = -800
LINES_3_SCORE = 10
LINES_4_SCORE = 20


class Player:

    def __init__(self):
        pass

    def setMaxIterationNumber(self, maxNumber):
        pass

    def setTypeOfAssignedMark(self, mark):
        self.mark = mark
        self.enemy_mark = 'X' if mark == 'O' else 'O'

    def setStateOfGameField(self, gameField):
        self.board = gameField

    def setInformationAboutDisqualification(self, info):
        pass

    def setInformationAboutGameEnd(self, info):
        pass

    def setInformationAboutWinning(self, info):
        pass

    def setLastMove(self, last_move):
        self.last_move = last_move

    def makeMove(self):
        my_possible_moves = get_possible_moves(self.board, self.enemy_mark)

        my_move_analyzer(my_possible_moves, self.board, self.mark, self.enemy_mark)
        empty_places_analyzer(my_possible_moves)
        enemy_move_analyzer(my_possible_moves, self.board, self.mark, self.enemy_mark)

        my_possible_moves.sort(key=lambda x: x[3], reverse=True)
        move = my_possible_moves[0]
        return self.mark, move[1], move[0], move[4]


def get_possible_moves(board, opponent_mark):
    possible_moves = []

    for i in range(5):
        if board[i][0] != opponent_mark:
            append_moves(possible_moves, i, 0, board[i][0])
        if board[0][i] != opponent_mark:
            append_moves(possible_moves, 0, i, board[0][i])
        if board[i][4] != opponent_mark:
            append_moves(possible_moves, i, 4, board[i][4])
        if board[4][i] != opponent_mark:
            append_moves(possible_moves, 4, i, board[4][i])

    return possible_moves


def append_moves(possible_moves, row, column, mark):
    possible_pushes = ['PUSH_DOWN', 'PUSH_UP', 'PUSH_RIGHT', 'PUSH_LEFT']

    if row == 0:
        possible_pushes.remove('PUSH_DOWN')
    if row == 4:
        possible_pushes.remove('PUSH_UP')
    if column == 0:
        possible_pushes.remove('PUSH_RIGHT')
    if column == 4:
        possible_pushes.remove('PUSH_LEFT')

    for push in possible_pushes:
        possible_moves.append([row, column, mark, 0, push])


def empty_places_analyzer(my_possible_moves):
    for my_move in my_possible_moves:
        if my_move[3] >= 0:
            if my_move[2] == " ":
                my_move[3] = my_move[3] + EMPTY_PLACE_SCORE
                if my_move[0] == 0 and my_move[1] == 0 or my_move[0] == 0 and my_move[1] == 4 or my_move[0] == 4 and \
                        my_move[1] == 0 or my_move[
                    0] == 4 and my_move[1] == 4:
                    my_move[3] = my_move[3] + EMPTY_CORNER_SCORE


def my_move_analyzer(my_possible_moves, board, my_mark, enemy_mark):
    for my_move in my_possible_moves:
        my_move_board = deepcopy(board)
        apply_move(my_move_board, my_move, my_mark)
        my_lines_after = find_lines_length(my_mark, my_move_board)
        enemy_lines_after = find_lines_length(enemy_mark, my_move_board)
        if my_lines_after[2] != 0 and enemy_lines_after[2] == 0:
            my_move[3] += (WIN_SCORE * 10)
        if my_lines_after[2] == 0 and enemy_lines_after[2] != 0:
            my_move[3] += (LOSE_SCORE * 10)
        if my_lines_after[2] != 0 and enemy_lines_after[2] != 0:
            my_move[3] += (DRAW_SCORE * 10)
        if my_move[3] >= 0:
            my_lines_before = find_lines_length(my_mark, board)
            score_lines_grow(my_move, my_lines_before, my_lines_after)


def score_lines_grow(my_move, lines_before, lines_after):
    length_3_score = (lines_after[0] - lines_before[0]) * LINES_3_SCORE
    length_4_score = (lines_after[1] - lines_before[1]) * LINES_4_SCORE
    my_move[3] += (length_3_score + length_4_score)


def enemy_move_analyzer(my_moves, board, my_mark, enemy_mark):
    for my_move in my_moves:
        if my_move[3] >= 0:
            my_move_board = deepcopy(board)
            apply_move(my_move_board, my_move, my_mark)
            enemy_moves = get_possible_moves(my_move_board, enemy_mark)
            can_lose = False
            can_draw = False
            for enemy_move in enemy_moves:
                enemy_move_board = deepcopy(my_move_board)
                apply_move(enemy_move_board, enemy_move, enemy_mark)
                my_lines = find_lines_length(my_mark, enemy_move_board)
                enemy_lines = find_lines_length(enemy_mark, enemy_move_board)
                if my_lines[2] == 0 and enemy_lines[2] != 0:
                    can_lose = True
                if my_lines[2] != 0 and enemy_lines[2] != 0:
                    can_draw = True
            if can_lose:
                my_move[3] += LOSE_SCORE
            if can_draw and not can_lose:
                my_move[3] += DRAW_SCORE


def apply_move(board, move, mark):
    (row, col, _, score, push_type) = move
    if push_type not in ['PUSH_DOWN', 'PUSH_UP', 'PUSH_RIGHT', 'PUSH_LEFT']:
        pass
    if push_type == 'PUSH_DOWN':
        push_down(board, row, col, mark)
    if push_type == 'PUSH_UP':
        push_up(board, row, col, mark)
    if push_type == 'PUSH_RIGHT':
        push_right(board, row, col, mark)
    if push_type == 'PUSH_LEFT':
        push_left(board, row, col, mark)


def push_down(board, row, col, mark):
    first_row = 0
    for i in range(row, first_row, -1):
        board[i][col] = board[i - 1][col]
    board[first_row][col] = mark


def push_up(board, row, col, mark):
    last_row = len(board) - 1
    for i in range(row, last_row):
        board[i][col] = board[i + 1][col]
    board[last_row][col] = mark


def push_right(board, row, col, mark):
    first_col = 0
    for i in range(col, first_col, -1):
        board[row][i] = board[row][i - 1]
    board[row][first_col] = mark


def push_left(board, row, col, mark):
    last_col = len(board) - 1
    for i in range(col, last_col):
        board[row][i] = board[row][i + 1]
    board[row][last_col] = mark


def find_lines_length(mark, board):
    vertically = check_vertically(mark, board)
    horizontally = check_horizontally(mark, board)
    diagonally = check_diagonally(mark, board)
    lines_length = [0, 0, 0]
    for i in range(3):
        lines_length[i] = vertically[i] + horizontally[i] + diagonally[i]
    return lines_length


def check_vertically(mark, board):
    lengths = [0, 0, 0]
    length = 0
    for i in range(5):
        for j in range(5):
            if board[j][i] == mark:
                length += 1
            else:
                if length > 2:
                    lengths[length - 3] += 1
                length = 0
        if length > 2:
            lengths[length - 3] += 1
        length = 0
    return lengths


def check_horizontally(mark, board):
    lengths = [0, 0, 0]
    length = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == mark:
                length += 1
            else:
                if length > 2:
                    lengths[length - 3] += 1
                length = 0
        if length > 2:
            lengths[length - 3] += 1
        length = 0
    return lengths


def check_diagonally(mark, board):
    lengths = [0, 0, 0]

    if board[2][0] == mark and board[3][1] == mark and board[4][2] == mark:
        lengths[0] += 1

    if board[1][0] == mark and board[2][1] == mark and board[3][2] == mark and board[4][3] == mark:
        lengths[1] += 1
    if board[2][1] == mark and board[3][2] == mark and board[4][3] == mark:
        lengths[0] += 1
    if board[1][0] == mark and board[2][1] == mark and board[3][2] == mark:
        lengths[0] += 1

    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark and board[3][3] == mark and board[4][
        4] == mark:
        lengths[2] += 1
    if board[1][1] == mark and board[2][2] == mark and board[3][3] == mark and board[4][4] == mark:
        lengths[1] += 1
    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark and board[3][3] == mark:
        lengths[1] += 1
    if board[2][2] == mark and board[3][3] == mark and board[4][4] == mark:
        lengths[0] += 1
    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
        lengths[0] += 1
    if board[1][1] == mark and board[2][2] == mark and board[3][3] == mark:
        lengths[0] += 1

    if board[0][1] == mark and board[1][2] == mark and board[2][3] == mark and board[3][4] == mark:
        lengths[1] += 1
    if board[1][2] == mark and board[2][3] == mark and board[3][4] == mark:
        lengths[0] += 1
    if board[0][1] == mark and board[1][2] == mark and board[2][3] == mark:
        lengths[0] += 1

    if board[0][2] == mark and board[1][3] == mark and board[2][4] == mark:
        lengths[0] += 1

    if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark:
        lengths[0] += 1

    if board[0][3] == mark and board[1][2] == mark and board[2][1] == mark and board[3][0] == mark:
        lengths[1] += 1
    if board[1][2] == mark and board[2][1] == mark and board[3][0] == mark:
        lengths[0] += 1
    if board[0][3] == mark and board[1][2] == mark and board[2][1] == mark:
        lengths[0] += 1

    if board[0][4] == mark and board[1][3] == mark and board[2][2] == mark and board[3][1] == mark and board[4][
        0] == mark:
        lengths[2] += 1
    if board[1][3] == mark and board[2][2] == mark and board[3][1] == mark and board[4][0] == mark:
        lengths[1] += 1
    if board[0][4] == mark and board[1][3] == mark and board[2][2] == mark and board[3][1] == mark:
        lengths[1] += 1
    if board[2][2] == mark and board[3][1] == mark and board[4][0] == mark:
        lengths[0] += 1
    if board[0][4] == mark and board[1][3] == mark and board[2][2] == mark:
        lengths[0] += 1
    if board[1][3] == mark and board[2][2] == mark and board[3][1] == mark:
        lengths[0] += 1

    if board[1][4] == mark and board[2][3] == mark and board[3][2] == mark and board[4][1] == mark:
        lengths[1] += 1
    if board[2][3] == mark and board[3][2] == mark and board[4][1] == mark:
        lengths[0] += 1
    if board[1][4] == mark and board[2][3] == mark and board[3][2] == mark:
        lengths[0] += 1

    if board[2][4] == mark and board[3][3] == mark and board[4][2] == mark:
        lengths[0] += 1

    return lengths
