import random


class Player:

    def __init__(self):
        pass

    def setMaxIterationNumber(self, maxNumber):
        self.iterations = maxNumber

    def setTypeOfAssignedMark(self, mark):
        self.mark = mark
        self.opponent_mark = 'X' if mark == 'O' else 'O'

    def setStateOfGameField(self, gameField):
        self.board = gameField

    def setInformationAboutDisqualification(self, info):
        pass

    def setInformationAboutGameEnd(self, info):
        pass

    def setInformationAboutWinning(self, info):
        pass

    def makeMove(self):
        possible_moves = []

        for i in range(5):
            if self.board[i][0] != self.opponent_mark:
                possible_moves.append((0, i))
            if self.board[0][i] != self.opponent_mark:
                possible_moves.append((i, 0))
            if self.board[i][4] != self.opponent_mark:
                possible_moves.append((4, i))
            if self.board[4][i] != self.opponent_mark:
                possible_moves.append((i, 4))

        move = random.choice(possible_moves)
        possible_pushs = ['PUSH_DOWN', 'PUSH_UP', 'PUSH_RIGHT', 'PUSH_LEFT']

        if move[0] == 0:
            possible_pushs.remove('PUSH_RIGHT')
        if move[0] == 4:
            possible_pushs.remove('PUSH_LEFT')
        if move[1] == 0:
            possible_pushs.remove('PUSH_DOWN')
        if move[1] == 4:
            possible_pushs.remove('PUSH_UP')

        push = random.choice(possible_pushs)

        return self.mark, move[0], move[1], push
