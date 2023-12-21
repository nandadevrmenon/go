from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction, QIcon

import sys
from SideBar import SideBar
from QuitDialog import QuitDialog
from board import Board
from PrimaryButton import PrimaryButton
import math

# from DrawingArea import DrawingArea

# from HelpDialog import HelpDialog
# from AboutDialog import AboutDialog


class GameScreen(QMainWindow):
    back_to_start_signal = pyqtSignal()

    def __init__(self, player1, player2):
        super().__init__()

        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = self.player1
        self.isGameRunning = True

        # set window appearance
        self.setWindowTitle("Go")
        self.setStyleSheet(
            """
            background-color: #141414;
            
            QMenuBar{
            background-color: #070114;
            color:white;
            }
            QMenu {
                background-color: #070114;
                color:white;
            }
            QMenu::item {
                color: white;
            }
        """
        )
        self.setMinimumWidth(1150)
        self.setMinimumHeight(700)

        self.play_area = QWidget()
        play_area_layout = QVBoxLayout()
        play_area_layout.setContentsMargins(0, 20, 0, 0)
        play_area_layout.setSpacing(0)
        self.play_area.setLayout(play_area_layout)

        button_dock = QWidget()
        button_dock_layout = QHBoxLayout()
        button_dock.setLayout(button_dock_layout)
        button_dock.setFixedHeight(100)

        undo_button = PrimaryButton("Undo", do_nothing)
        redo_button = PrimaryButton("Redo", do_nothing)
        pass_button = PrimaryButton("Pass", do_nothing)
        resign_button = PrimaryButton("Resign", do_nothing)
        pause_button = PrimaryButton("Pause", do_nothing)

        button_dock_layout.addWidget(undo_button)
        button_dock_layout.addWidget(redo_button)
        button_dock_layout.addWidget(pass_button)
        button_dock_layout.addWidget(resign_button)
        button_dock_layout.addWidget(pause_button)

        self.board = Board()

        play_area_layout.addWidget(self.board)
        play_area_layout.addWidget(button_dock)

        # create a Side bar into which the player info is passed (so it can create dialogs using that info which is readily available)
        self.p1_side = SideBar(
            player1,
            False,
            self.back_to_start_signal,  # pass in the custom signal that makes the start screen open back up
        )

        self.p2_side = SideBar(
            player2,
            True,
            self.back_to_start_signal,  # pass in the custom signal that makes the start screen open back up
        )

        # define and adjust main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.p1_side)
        main_layout.addWidget(self.play_area)
        main_layout.addWidget(self.p2_side)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)


def do_nothing():
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameScreen("bruh", "hello")  # open the start screen of the game
    window.show()
    app.exec()  # start the event loop running
