from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QSpacerItem,
    QApplication,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
)
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

    def __init__(self, p1Name, p2Name, is_speed_go, is_handicap):
        super().__init__()
        self.board = Board(self.try_move)

        self.is_game_running = True
        self.is_game_started = False
        self.game_logic = GameLogic(p1Name, p2Name)
        self.is_speed_go = is_speed_go
        self.is_handicap = is_handicap

        self.passed = False

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
        self.setMinimumHeight(750)

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
        resign_button = PrimaryButton("Resign", self.resign_from_game)
        pause_button = PrimaryButton("Pause", do_nothing)
        reset_button = PrimaryButton("Reset", self.reset_game)

        spacer = QSpacerItem(
            40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        button_dock_layout.addStretch()
        button_dock_layout.addWidget(undo_button)
        button_dock_layout.addWidget(redo_button)
        button_dock_layout.addSpacerItem(spacer)
        button_dock_layout.addWidget(pass_button)
        button_dock_layout.addWidget(resign_button)
        button_dock_layout.addWidget(pause_button)
        button_dock_layout.addWidget(reset_button)
        button_dock_layout.addStretch()

        center_board = QHBoxLayout()

        center_board.addStretch()
        center_board.addWidget(self.board)
        center_board.addStretch()

        play_area_layout.addLayout(center_board)
        play_area_layout.addWidget(button_dock)

        # create a Side bar into which the player info is passed (so it can create dialogs using that info which is readily available)
        self.p1_side = SideBar(
            GameLogic.player1,
            has_kumi=False,
            starts_first=not is_handicap,
            is_speed_go=self.is_speed_go,
        )

        self.p2_side = SideBar(
            GameLogic.player2,
            has_kumi=True,
            starts_first=is_handicap,
            is_speed_go=self.is_speed_go,
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

    def start_game(self):
        self.switch_timers()

    def check_passes(self):
        if self.passed:
            self.end_game()
        else:
            GameLogic.flip_turn()
            self.passed = True
            self.switch_timers()

    def reset_game(self):
        print("baord being reset")
        self.game_logic.reset_board()
        GameLogic.player1["score"] = [0, 0]
        GameLogic.player2["score"] = [0, 0]

        self.p1_side.update_score()
        self.p2_side.update_score()
        if self.is_speed_go:
            self.p1_side.reset_timer()
            self.p2_side.reset_timer()
        self.p1_side.default_turn_animation()
        self.p2_side.default_turn_animation()

        self.redraw_board()

    def undo_board(self):
        if GameLogic.undo_board():
            self.switch_timers()
            self.redraw_board()

    def redo_board(self):
        if GameLogic.redo_board():
            self.switch_timers()
            self.redraw_board()

    def resign_from_game(self):
        # show which plyer lost in the Reisgn dialog and thats the end of it .
        print(GameLogic.current_player["name"], "has resigned")
        pass

    def try_move(self, y, x):
        try:
            type = 1 if GameLogic.current_player is GameLogic.player1 else 2
            return GameLogic.try_move(type, y, x)
        finally:
            self.redraw_board()
            self.p1_side.update_score()
            self.p2_side.update_score()
            self.switch_timers()
            self.passed = False

    def redraw_board(self):
        self.board.update()

    def end_game(self):
        # FLORRYN
        # call the game end dialogue and edit it so that it calculated the scores and displays it tot he suer. you might have to change the colours as well.
        pass

    def switch_timers(self):
        if GameLogic.current_player == GameLogic.player1:
            if self.is_speed_go:
                GameLogic.player1["timer"].start()  # stop the timer for player 1
                GameLogic.player2["timer"].stop()
            self.p1_side.start_turn_animation()
            self.p2_side.stop_turn_animation()

        else:
            if self.is_speed_go:
                GameLogic.player2["timer"].start()  # stop the timer for player 1
                GameLogic.player1["timer"].stop()
            self.p2_side.start_turn_animation()
            self.p1_side.stop_turn_animation()


def do_nothing():
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameScreen(
        "bruh", "hello", False, False
    )  # open the start screen of the game
    window.show()
    app.exec()  # start the event loop running
