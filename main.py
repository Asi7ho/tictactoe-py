import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400


# Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.game = Game()

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
        vbox = QVBoxLayout()

        ###
        # ui
        ###
        title = QLabel("Tic Tac Toe")
        newGameButton = QPushButton("New Game")
        newGameButton.clicked.connect(self.gamePage)

        ###
        # create layout with ui components
        # - title at the top
        # - newGame button at the center of the window
        ###

        vbox.addWidget(title, alignment=Qt.AlignCenter)
        vbox.addStretch(1)

        vbox.addWidget(newGameButton, alignment=Qt.AlignCenter)
        vbox.addStretch(1)

        ###
        # central widget
        ###
        widget = QWidget()

        widget.setLayout(vbox)
        self.setCentralWidget(widget)

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
        buttons = {}
        for i in range(3):
            for j in range(3):
                # keep a reference to the buttons
                buttons[(i, j)] = QPushButton()

        resetButton = QPushButton("Reset")
        resetButton.clicked.connect(self.gamePage)

        quitButton = QPushButton("Quit")
        quitButton.clicked.connect(sys.exit)

        ###
        # create layout with ui components
        # - grid at the top
        # - reset and quit buttons at the bottom of the window
        ###
        for i in range(3):
            for j in range(3):
                gridLayout.addWidget(buttons[(i, j)], i, j)

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


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
