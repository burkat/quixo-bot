from random import *
from sys import *
from copy import *

PLAYER_MARKS = ['O', 'X']
INPUT_STATE_MARK = ' '
BOARD_SIZE = 5
NUMBER_OF_MOVES = 100

LOGS_BOARD = False

PUSH_DOWN = 'PUSH_DOWN'
PUSH_UP = 'PUSH_UP'
PUSH_RIGHT = 'PUSH_RIGHT'
PUSH_LEFT = 'PUSH_LEFT'
DIRECTIONS = [PUSH_DOWN, PUSH_UP, PUSH_RIGHT, PUSH_LEFT]
MIN = 0
MAX = BOARD_SIZE - 1
LIMITS = [MIN, MAX]
CORNERS = [(x, y) for x in LIMITS for y in LIMITS]
SIDES = [(x, y) for x in LIMITS for y in range(MIN + 1, MAX)] + [(x, y) for y in LIMITS for x in range(MIN + 1, MAX)]
BORDER = CORNERS + SIDES


def main(names_of_gamers):
    players = create_players(NUMBER_OF_MOVES, names_of_gamers)
    board = create_empty_board(BOARD_SIZE)
    if LOGS_BOARD:
        print_board(board)
    result = []
    game_end = False
    disq = False
    i = 0
    while (i < NUMBER_OF_MOVES) and (game_end == False):
        for ((player, name), mark) in zip(players, PLAYER_MARKS):
            if game_end == False:
                # Set board in player
                player.setStateOfGameField(deepcopy(board))
                # Make move by player
                move = player.makeMove()
                print(move)
                # Check if the move is valid
                (game_end, result, disq) = check_disqualification(board, players, player, name, mark, move)
                if disq:
                    print('EX> Disqualification')
                    player.setInformationAboutDisqualification(True)
                else:
                    player.setInformationAboutDisqualification(False)
                if disq == False:
                    apply_move(board, move)
                if LOGS_BOARD:
                    print_board(board)
                if game_end == False:
                    (game_end, result) = check_wining_condition(board, BOARD_SIZE, players)
        i += 1
    if game_end == False:
        result = [('O', players[0][1], False, False), ('X', players[1][1], False, False)]
        print('EX> Number of iterations exceeded. No one won.')
    players[0][0].setInformationAboutGameEnd(True)
    players[1][0].setInformationAboutGameEnd(True)
    players[0][0].setInformationAboutWinning(result[0][2])
    players[1][0].setInformationAboutWinning(result[1][2])
    return (result, i)


def _target_coords(x, y, direction):
    if direction == PUSH_UP:
        return x, MAX
    if direction == PUSH_DOWN:
        return x, MIN
    if direction == PUSH_LEFT:
        return MAX, y
    if direction == PUSH_RIGHT:
        return MIN, y
    return None


def _all_moves(mark):
    return [(mark, x, y, direction) for (x, y) in BORDER for direction in DIRECTIONS]


def _possible_moves(board, players, player, name, mark, move):
    return [(mark, x, y, direction) for (mark, x, y, direction) in _all_moves(mark) if
            (x, y) != _target_coords(x, y, direction)]


def _legal_moves(board, players, player, name, mark, move):
    return [(mark, x, y, direction) for (mark, x, y, direction) in
            _possible_moves(board, players, player, name, mark, move) if
            board[y][x] in [INPUT_STATE_MARK, mark]]


def check_disqualification(board, players, player, name, mark, move):
    if move in _legal_moves(board, players, player, name, mark, move):
        return (False, [], False)
    else:
        if mark == 'X':
            finish_game('RES> ' + get_wining_message('O'))
            return (True, [('O', players[0][1], True, False), ('X', players[1][1], False, True)], True)
        else:
            finish_game('RES> ' + get_wining_message('X'))
            return (True, [('O', players[0][1], False, True), ('X', players[1][1], True, False)], True)


def create_players(number_of_moves, names_of_gamers):
    return [(create_player(number_of_moves, mark, name), name) for mark, name in zip(PLAYER_MARKS, names_of_gamers)]


def create_player(iterations, mark, name):
    P = __import__(name)
    player = P.Player()
    player.setInformationAboutDisqualification(False)
    player.setInformationAboutGameEnd(False)
    player.setMaxIterationNumber(deepcopy(iterations))
    player.setTypeOfAssignedMark(deepcopy(mark))
    return player


def create_empty_board(board_size):
    return [[INPUT_STATE_MARK for _ in range(board_size)] for _ in range(board_size)]


def print_board(board):
    for row in board:
        print(row)


def apply_move(board, move):
    (mark, col, row, push_type) = move
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


def check_wining_condition(board, board_size, players):
    marks_in_rows, marks_in_cols, marks_in_left, marks_in_right = count_marks_in_rows_cols_and_diagonals(board_size,
                                                                                                         board)
    circles_won = has_mark_won(board_size, marks_in_rows, marks_in_cols, marks_in_left, marks_in_right, 'O')
    crosses_won = has_mark_won(board_size, marks_in_rows, marks_in_cols, marks_in_left, marks_in_right, 'X')
    if circles_won and crosses_won:
        finish_game('RES> Players have tied the game!')
        return (True, [('O', players[0][1], True, False), ('X', players[1][1], True, False)])
    if circles_won:
        finish_game('RES> ' + get_wining_message('O'))
        return (True, [('O', players[0][1], True, False), ('X', players[1][1], False, False)])
    if crosses_won:
        finish_game('RES> ' + get_wining_message('X'))
        return (True, [('O', players[0][1], False, False), ('X', players[1][1], True, False)])
    return (False, [])


def count_marks_in_rows_cols_and_diagonals(board_size, board):
    marks_in_rows, marks_in_cols = {}, {}
    marks_in_left_to_right_diagonal = create_marks_in_diagonal_dict()
    marks_in_right_to_left_diagonal = create_marks_in_diagonal_dict()
    for row in range(board_size):
        for col in range(board_size):
            mark = board[row][col]
            update_dict(marks_in_rows, row, mark)
            update_dict(marks_in_cols, col, mark)
            if row == col:
                marks_in_left_to_right_diagonal[mark] += 1
            if row == BOARD_SIZE - 1 - col:
                marks_in_right_to_left_diagonal[mark] += 1
    return marks_in_rows, marks_in_cols, marks_in_left_to_right_diagonal, marks_in_right_to_left_diagonal


def create_marks_in_diagonal_dict():
    return {mark: 0 for mark in [*PLAYER_MARKS, INPUT_STATE_MARK]}


def update_dict(dictionary, index, mark):
    try:
        dictionary[index][mark] += 1
    except KeyError:
        try:
            dictionary[index][mark] = 1
        except KeyError:
            dictionary[index] = {mark: 1}


def has_mark_won(board_size, marks_in_rows, marks_in_cols, marks_in_left, marks_in_right, mark):
    return check_wining_condition_for_rows_and_cols(board_size, marks_in_rows, marks_in_cols, mark) \
           or check_winning_condition_for_diagonals(marks_in_left, marks_in_right, board_size, mark)


def check_wining_condition_for_rows_and_cols(board_size, marks_in_rows, marks_in_cols, mark):
    mark_has_won = False
    for index in range(board_size):
        try:
            if marks_in_rows[index][mark] == board_size or marks_in_cols[index][mark] == board_size:
                return True
        except KeyError:
            pass
    return mark_has_won


def check_winning_condition_for_diagonals(marks_in_left_to_right, marks_in_right_to_left, board_size, mark):
    if marks_in_left_to_right[mark] == board_size or marks_in_right_to_left[mark] == board_size:
        return True
    return False


def finish_game(message):
    print(message)


def get_wining_message(mark):
    return f"Player with mark '{mark}' has won the game!"


if __name__ == "__main__":
    seed()
    if len(argv) != 3:
        print("Wellcome to:")
        print("The Fast and Furious 'X' and 'O' game!!")
        print("e.g.    game player1 player2")
        exit()
    for x in range(1000):
        (res, iter) = main(argv[1:])
        print(res)
