import sys
from functools import partial
from math import inf

from ai import AI

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

GRID_HEIGHT = 330


# Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.board_size = 3
        self.icon_size = GRID_HEIGHT / self.board_size
        self.game = AI(self.board_size)
        self.buttons = {}

        # window
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # launch
        self.homePage()
        self.show()

    def homePage(self):
        ####
        # layout
        ###
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        ###
        # ui
        ###
        title = QLabel("Tic Tac Toe")
        newGameButton = QPushButton("New Game")
        newGameButton.clicked.connect(self.gamePage)

        boardSizeLabel = QLabel("Board Size: {} x {}".format(
            self.board_size, self.board_size))

        plusButton = QPushButton("+")
        plusButton.clicked.connect(self.increaseBoard)

        minusButton = QPushButton("-")
        minusButton.clicked.connect(self.decreaseBoard)

        if self.board_size == 3:
            minusButton.setEnabled(False)

        ###
        # create layout with ui components
        # - title at the top
        # - newGame button at the center of the window
        ###
        hbox.addStretch(1)
        hbox.addWidget(boardSizeLabel)
        hbox.addWidget(plusButton)
        hbox.addWidget(minusButton)
        hbox.addStretch(1)

        vbox.addWidget(title, alignment=Qt.AlignCenter)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addWidget(newGameButton, alignment=Qt.AlignCenter)
        vbox.addStretch(1)

        ###
        # central widget
        ###
        widget = QWidget()

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def increaseBoard(self):
        self.board_size += 1
        self.icon_size = GRID_HEIGHT / self.board_size
        self.game = AI(self.board_size)
        self.homePage()

    def decreaseBoard(self):
        self.board_size -= 1
        self.icon_size = GRID_HEIGHT / self.board_size
        self.game = AI(self.board_size)
        self.homePage()

    def gamePage(self):
        ###
        # layout
        ###
        gridLayout = QGridLayout()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        ###
        # ui components
        ###
        for i in range(self.board_size):
            for j in range(self.board_size):
                # keep a reference to the buttons
                self.buttons[(i, j)] = QPushButton()
                self.buttons[(i, j)].setIcon(QIcon(self.game.EMPTY))
                self.buttons[(i, j)].setIconSize(
                    QSize(int(self.icon_size), int(self.icon_size)))
                self.buttons[(i, j)].clicked.connect(
                    partial(self.setAction, i, j))

        resetButton = QPushButton("Reset")
        resetButton.clicked.connect(self.reset)

        quitButton = QPushButton("Quit")
        quitButton.clicked.connect(sys.exit)

        ###
        # create layout with ui components
        # - grid at the top
        # - reset and quit buttons at the bottom of the window
        ###
        for i in range(self.board_size):
            for j in range(self.board_size):
                gridLayout.addWidget(self.buttons[(i, j)], i, j)

        # buttons at the bottom of the window
        vbox.addLayout(gridLayout)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox.addWidget(resetButton)
        hbox.addWidget(quitButton)

        ###
        # central widget
        ###
        widget = QWidget()

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    def reset(self):
        self.game.resetGame()
        self.gamePage()

    def setAction(self, i, j):
        # set move for the player
        self.game.setMove(i, j, self.game.player)
        self.buttons[(i, j)].setIcon(QIcon(self.game.player))
        self.buttons[(i, j)].setIconSize(QSize(self.icon_size, self.icon_size))
        self.buttons[(i, j)].setEnabled(False)
        if self.checkEndGame():
            return

        # set move for the computer
        self.game.flipPlayer()

        depth = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.game.board[row][col] == self.game.EMPTY:
                    depth += 1

        alpha = -inf
        beta = +inf
        depth = min(depth, self.game.max_depth)
        move = self.game.minimax(depth, alpha, beta)
        x = move[0]
        y = move[1]
        self.game.setMove(x, y, self.game.player)
        self.buttons[(x, y)].setIcon(QIcon(self.game.player))
        self.buttons[(x, y)].setIconSize(QSize(self.icon_size, self.icon_size))
        self.buttons[(x, y)].setEnabled(False)
        if self.checkEndGame():
            return

        self.game.flipPlayer()

    def checkEndGame(self):
        endGame = False
        if self.game.checkWin(self.game.player):
            for x in range(self.board_size):
                for y in range(self.board_size):
                    self.buttons[(x, y)].setEnabled(False)

            msg = QMessageBox()
            msg.setText(self.game.winner + " won")
            x = msg.exec_()
            endGame = True

        if self.game.checkTie():
            msg = QMessageBox()
            msg.setText("Tie")
            x = msg.exec_()
            endGame = True

        return endGame


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
