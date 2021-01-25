# Imports
import numpy as np


class TicTacToe(object):
    def __init__(self, board_size):
        self.nb_to_win = 3
        self.board_size = board_size
        self.board = np.empty([self.board_size, self.board_size], dtype='U32')

        self.EMPTY = './assets/empty.png'
        self.HUMAN = './assets/cross.png'
        self.COMPUTER = './assets/circle.png'

        self.winner = ''

        self.initialize_board()

        # First to play
        self.player = self.HUMAN

    def initialize_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.board[row][col] = self.EMPTY

    def resetGame(self):
        self.board = np.empty([self.board_size, self.board_size], dtype='U32')

        self.initialize_board()

        self.winner = ''

        # First to play
        self.player = self.HUMAN

    def checkWin(self, player):
        """
        Check if there is a winner
        :param player: Players turn
        :return: True if there is a win, False otherwise
        """

        # check rows
        rows = []
        for row in range(self.board_size):
            subarray = find_subarray(self.board[row, :], self.nb_to_win)
            for j in range(len(subarray)):
                rows.append(subarray[j])

        # check columns
        cols = []
        for col in range(self.board_size):
            subarray = find_subarray(self.board[:, col], self.nb_to_win)
            for j in range(len(subarray)):
                cols.append(subarray[j])

        # check diagonals
        diags = []
        for diag in range(-self.board_size + 1, self.board_size):
            subarray = find_subarray(
                self.board.diagonal(offset=diag), self.nb_to_win)
            if not subarray:
                continue
            for j in range(len(subarray)):
                diags.append(subarray[j])

        for diag in range(-self.board_size + 1, self.board_size):
            subarray = find_subarray(
                np.fliplr(self.board).diagonal(offset=diag), self.nb_to_win)
            if not subarray:
                continue
            for j in range(len(subarray)):
                diags.append(subarray[j])

        win_state = np.concatenate((rows, cols, diags))
        win_condition = np.full([1, self.nb_to_win], player)

        if (win_condition == win_state).all(1).any():
            if self.player == self.COMPUTER:
                self.winner = 'Computer'
            else:
                self.winner = 'You'
            return True
        else:
            return False

    def checkTie(self):
        """
        check if there is a tie
        :return True if tie, false otherwise
        """

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == self.EMPTY:
                    return False

        return True

    def gameOver(self):
        """
        Check if the human or the computer wins
        :return: True if the computer or the human wins
        """
        if self.checkWin(self.COMPUTER):
            self.winner = "Computer"
        elif self.checkWin(self.HUMAN):
            self.winner = "You"

        return self.checkWin(self.COMPUTER) or self.checkWin(self.HUMAN)

    def moveIsValid(self, x, y):
        """
        Check if a move is valid (the cell is empty)
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if board[x][y] is empty
        """
        if self.board[x][y] == self.EMPTY:
            return True
        else:
            return False

    def setMove(self, x, y, player):
        """
        Set a move on the board
        :param player: players turn
        :param x: X coordinate
        :param y: Y coordinate
        :return: Set X or O on board[x][y]
        """
        if self.moveIsValid(x, y):
            self.board[x][y] = player

    def getEmptyCells(self):
        """
        get a list of the empty cells in the board
        :return: a list of the empty cells in the board
        """
        cells = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == self.EMPTY:
                    cells.append([row, col])

        return cells

    def flipPlayer(self):
        """
        Its at the other player to set a move
        """

        if self.player == self.HUMAN:
            self.player = self.COMPUTER
        else:
            self.player = self.HUMAN


def find_subarray(array, length):
    # store all the sublists
    sublist = []

    # first loop
    for i in range(len(array) + 1):

        # second loop
        for j in range(i + 1, len(array) + 1):
            # slice the subarray
            sub = array[i:j]
            if len(sub) == length:
                sublist.append(sub)

    return sublist
