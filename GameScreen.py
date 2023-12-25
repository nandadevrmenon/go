from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon

import sys
from SideBar import SideBar
from QuitDialog import QuitDialog
from board import Board
from PrimaryButton import PrimaryButton
import math

from game_logic import GameLogic

# from DrawingArea import DrawingArea
# from HelpDialog import HelpDialog
# from AboutDialog import AboutDialog


class GameScreen(QMainWindow):
    back_to_start_signal = pyqtSignal()

    def __init__(self, p1Name, p2Name):
        super().__init__()

        self.player1 = {"name": p1Name, "score": [12, 2], "timer": QTimer()}
        self.player2 = {"name": p2Name, "score": [1, 78], "timer": QTimer()}
        self.current_player = self.player1
        self.is_game_running = True
        self.is_game_started = False
        self.game_logic = GameLogic(self.player1, self.player2)

        self.passed = False

        game_state = [
            self.player1,
            self.player2,
            self.current_player,
            self.is_game_started,
            self.is_game_running,
            self.game_logic,
        ]

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
        # play_area_layout.setSpacing(0)
        self.play_area.setLayout(play_area_layout)

        button_dock = QWidget()
        button_dock_layout = QHBoxLayout()
        button_dock.setLayout(button_dock_layout)
        button_dock.setFixedHeight(100)

        undo_button = PrimaryButton("Undo", self.undo_board)
        redo_button = PrimaryButton("Redo", self.redo_board)
        pass_button = PrimaryButton("Pass", self.check_passes)
        resign_button = PrimaryButton("Resign", do_nothing)
        pause_button = PrimaryButton("Pause", do_nothing)
        reset_button = PrimaryButton("Reset", self.reset_game)

        button_dock_layout.addWidget(undo_button)
        button_dock_layout.addWidget(redo_button)
        button_dock_layout.addWidget(pass_button)
        button_dock_layout.addWidget(resign_button)
        button_dock_layout.addWidget(pause_button)
        button_dock_layout.addWidget(reset_button)

        center_board = QHBoxLayout()
        self.board = Board(game_state)

        center_board.addStretch()
        center_board.addWidget(self.board)
        center_board.addStretch()

        play_area_layout.addLayout(center_board)
        play_area_layout.addWidget(button_dock)

        # create a Side bar into which the player info is passed (so it can create dialogs using that info which is readily available)
        self.p1_side = SideBar(
            self.player1,
            False,
        )

        self.p2_side = SideBar(
            self.player2,
            True,
        )

        indicate_player_turn(self)

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

    def check_passes(self):
        if self.passed:
            self.reset_game()
            self.end_game()
        else:
            self.passed = True

    def reset_game(self):
        print("baord being reset")
        self.game_logic.reset_board()
        self.player1["score"] = [0, 0]
        self.player2["score"] = [0, 0]

        self.p1_side.update_score()
        self.p1_side.reset_timer()
        self.p2_side.update_score()
        self.p2_side.reset_timer()
        self.indicate_player_turn()

        self.redraw_board()

        # then redraw an empty board ( or basically call theupdate board method. that basically redarws theboard according to the static vairblae board in the GameLogic class)

    def undo_board(self):
        GameLogic.undo_board()
        indicate_player_turn(self)
        # redraw board()

    def redo_board(self):
        GameLogic.redo_board()
        indicate_player_turn(self)  

    def redraw_board(self):
        pass

    def end_game(self):
        pass

def do_nothing():
    pass

def indicate_player_turn(self):
    if self.current_player == self.player1:
        self.p1_side.turn_label.setHidden(False)
        self.p2_side.turn_label.setHidden(True)
    if self.current_player == self.player2:
        self.p1_side.turn_label.setHidden(True)
        self.p2_side.turn_label.setHidden(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameScreen("bruh", "hello")  # open the start screen of the game
    window.show()
    app.exec()  # start the event loop running
