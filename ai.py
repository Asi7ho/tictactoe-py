from math import inf

from game import TicTacToe


class AI(TicTacToe):
    def __init__(self, board_size):
        super().__init__(board_size)

        self.max_depth = 8

    def evaluate(self):
        """
        Evaluation of the board
        :return: return the score (+1 if computer wins, -1 if human wins)
        """

        if self.checkWin(self.COMPUTER):
            score = +1
        elif self.checkWin(self.HUMAN):
            score = -1
        else:
            score = 0

        return score

    def minimax(self, depth, alpha, beta):
        """
            AI function that choose the best move
            :param depth: node index in the tree
            :return: list with [best_row, best_col, best_score]
            """

        player_stk = self.player
        cells = self.getEmptyCells()

        if self.player == self.COMPUTER:
            best = [-1, -1, -inf]
        else:
            best = [-1, -1, +inf]

        if depth == 0 or self.gameOver():
            score = self.evaluate()
            return [-1, -1, score]

        for cell in cells:
            row = cell[0]
            col = cell[1]

            self.board[row][col] = self.player
            self.flipPlayer()
            score = self.minimax(depth - 1, alpha, beta)
            self.board[row][col] = self.EMPTY

            score[0], score[1] = row, col

            self.player = player_stk
            if self.player == self.COMPUTER:
                if score[-1] > best[-1]:
                    best = score

                alpha = max(alpha, best[-1])
            else:
                if score[-1] < best[-1]:
                    best = score

                beta = min(beta, best[-1])

            if alpha >= beta:
                break

        return best
