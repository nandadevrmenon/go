from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QSpacerItem,
    QApplication,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
)
from PyQt6.QtCore import pyqtBoundSignal, pyqtSignal
from PyQt6.QtGui import QAction, QIcon

import sys
from SideBar import SideBar
from QuitDialog import QuitDialog
from board import Board
from PrimaryButton import PrimaryButton

from game_logic import GameLogic
from GameEndDialogue import GameEndDialog
from IconButton import IconButton
from PauseDialog import PauseDialog
from HelpDialog import HelpDialog
from ResignDialog import ResignDialog
from AboutDialog import AboutDialog


class GameScreen(QMainWindow):
    def __init__(self, p1Name, p2Name, is_speed_go, is_handicap, back_to_start_signal):
        super().__init__()
        self.board = Board(self.try_move)
        self.back_to_start_signal = (
            back_to_start_signal  # signal that when emitted goes back to start screen
        )
        self.game_logic = GameLogic(
            p1Name, p2Name
        )  # create an instanc eof the game logic class while passing in the player names
        self.is_speed_go = is_speed_go  # speed go mode
        self.is_handicap = is_handicap

        self.passed = False  # variable to check for 2 passes

        self.help_dialog = HelpDialog(
            self
        )  # create a help dialog  but dont show it yet

        # set window appearance
        self.setWindowTitle("Go")
        self.setStyleSheet(
            """
            background-color: #141414;
            
            QMenuBar{
            background-color: #141414;
            color:white;
            }
            QMenu {
                background-color: #141414;
                color:white;
            }
            QMenu::item {
                color: white;
            }
        """
        )

        self.setMinimumWidth(1150)
        self.setMinimumHeight(750)

        # play are that include both the baord and the button dock
        self.play_area = QWidget()
        play_area_layout = QVBoxLayout()
        play_area_layout.setContentsMargins(0, 20, 0, 0)
        # play_area_layout.setSpacing(0)
        self.play_area.setLayout(play_area_layout)

        button_dock = QWidget()
        button_dock_layout = QHBoxLayout()
        button_dock.setLayout(button_dock_layout)
        button_dock.setFixedHeight(100)

        undo_icon = QIcon("images/undo.png")
        redo_icon = QIcon("images/redo.png")

        self.undo_button = IconButton(
            undo_icon,
            self.undo_board,
            (
                "Disabled in Speed Go" if is_speed_go else "Undo Move"
            ),  # make it disabled in speed go mode
        )
        self.redo_button = IconButton(
            redo_icon,
            self.redo_board,
            (
                "Disabled in Speed Go" if is_speed_go else "Redo Move"
            ),  # make it diabled in speed go mode
        )
        self.undo_button.setDisabled(True)
        self.redo_button.setDisabled(True)
        pass_button = PrimaryButton("Pass", self.check_passes)
        resign_button = PrimaryButton("Resign", self.resign_from_game)
        pause_button = PrimaryButton("Pause", self.pause_game)
        reset_button = PrimaryButton("Reset", self.reset_game)

        spacer = QSpacerItem(
            40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        button_dock_layout.addStretch()
        button_dock_layout.addWidget(self.undo_button)
        button_dock_layout.addWidget(self.redo_button)
        button_dock_layout.addSpacerItem(spacer)
        button_dock_layout.addWidget(pass_button)
        button_dock_layout.addWidget(resign_button)
        if not self.is_speed_go:  # add reset button if not in speed go
            button_dock_layout.addWidget(reset_button)
            del pause_button
        else:  # if in speed go mode
            del reset_button
            button_dock_layout.addWidget(
                pause_button
            )  # add the pause button to stop the timers
        button_dock_layout.addStretch()

        center_board = QHBoxLayout()

        center_board.addStretch()
        center_board.addWidget(self.board)
        center_board.addStretch()

        play_area_layout.addLayout(center_board)
        play_area_layout.addWidget(button_dock)

        # create a Side bar into which the player info is passed (so it can create dialogs using that info which is readily available)
        self.p1_side = SideBar(  # side bar for player 1 info
            GameLogic.player1,
            has_kumi=False,
            starts_first=not is_handicap,
            is_speed_go=self.is_speed_go,
            resign_callback=self.resign_from_game,
        )

        self.p2_side = SideBar(  # side bar for player 2 info
            GameLogic.player2,
            has_kumi=True,
            starts_first=is_handicap,
            is_speed_go=self.is_speed_go,
            resign_callback=self.resign_from_game,
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

        # create a menu bar
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)

        # 3 menu buttons game, move, and help
        game_menu = mainMenu.addMenu("Game")
        move_menu = mainMenu.addMenu("Move")
        help_menu = mainMenu.addMenu("Help")

        # pause action
        pause_action = QAction("Pause", self)
        pause_action.setShortcut("Space")  # set keyboard shortcut
        game_menu.addAction(pause_action)
        if not is_speed_go:
            pause_action.setEnabled(False)
        pause_action.triggered.connect(self.pause_game)

        # pass player turn
        pass_action = QAction("Pass", self)
        pass_action.setShortcut("Ctrl+P")  # set keyboard shortcut
        game_menu.addAction(pass_action)
        pass_action.triggered.connect(self.check_passes)

        # resign from the game
        resign_action = QAction("Resign", self)
        resign_action.setShortcut("Ctrl+X")
        resign_action.triggered.connect(self.resign_from_game)
        game_menu.addAction(resign_action)

        # reset the board
        reset_action = QAction("Reset", self)
        reset_action.setShortcut("Ctrl+R")
        game_menu.addAction(reset_action)
        if is_speed_go:
            reset_action.setEnabled(False)
        reset_action.triggered.connect(self.reset_game)

        # undo last move
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("U")
        undo_action.triggered.connect(self.undo_board)
        if is_speed_go:
            undo_action.setEnabled(False)
        move_menu.addAction(undo_action)

        # redo the last move that was undone
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("R")
        redo_action.triggered.connect(self.redo_board)
        if is_speed_go:
            redo_action.setEnabled(False)
        move_menu.addAction(redo_action)

        # game rules section shortcut
        help = QAction("Instructions", self)
        help.setShortcut("I")
        help_menu.addAction(help)
        help.triggered.connect(self.instruction_widget)

        # about the game short cut
        about = QAction("About", self)
        about.setShortcut("A")
        help_menu.addAction(about)
        about.triggered.connect(self.open_about_dialog)

    def try_move(
        self, y, x
    ):  # checks if the proposed move is possible and is not a suicide or KO or invalid move
        try:
            type = (
                1 if GameLogic.current_player is GameLogic.player1 else 2
            )  # which colour piece to place
            return GameLogic.try_move(type, y, x)
        finally:
            self.p1_side.update_score()  # after every move update the scores
            self.p2_side.update_score()
            self.switch_timers()  # switch the timers if turn has been switched
            self.passed = False  # reset the passed variable
            if (
                not self.is_speed_go
            ):  # if not speed go then disable or enable the undo redo buttons depending on wether states are available
                self.undo_button.setDisabled(not GameLogic.undo_is_possible())
                self.redo_button.setDisabled(not GameLogic.redo_is_possible())

    def check_passes(
        self,
    ):  # checks is one pass has already been made and if yes then ends game
        print(self.passed)
        if self.passed:
            self.end_game()
        else:
            GameLogic.flip_turn()  # changes the current player
            self.passed = True
            self.switch_timers()  # switch the timers

    def reset_game(
        self,
    ):  # resets the logical board and score and also updates the UI to go into the default state
        print("baord being reset")
        self.game_logic.reset_board()
        GameLogic.player1["score"] = [0, 0]
        GameLogic.player2["score"] = [0, 0]
        self.undo_button.setDisabled(True)
        self.redo_button.setDisabled(True)
        self.p1_side.update_score()
        self.p2_side.update_score()
        if self.is_speed_go:
            self.p1_side.reset_timer()
            self.p2_side.reset_timer()
        self.p1_side.default_turn_animation()
        self.p2_side.default_turn_animation()

        self.board.move_validity = None
        self.redraw_board()

    def undo_board(self):
        if GameLogic.undo_board():  # undo the move logically
            # update the UI to reflect that change
            self.switch_timers()
            self.redraw_board()
            self.p1_side.update_score()
            self.p2_side.update_score()
            self.redo_button.setDisabled(False)
            self.undo_button.setDisabled(not GameLogic.undo_is_possible())

    def redo_board(self):  # redo the move logically
        # update the UI to reflexxt the change
        if GameLogic.redo_board():
            self.switch_timers()
            self.redraw_board()
            self.p1_side.update_score()
            self.p2_side.update_score()
            self.undo_button.setDisabled(False)
            self.redo_button.setDisabled(not GameLogic.redo_is_possible())

    def resign_from_game(self):  # the player who calls this function loses immediately
        dialog = ResignDialog(
            self.reset_game, self.back_to_start_signal
        )  # we show the resign dialog
        dialog.exec()
        self.help_dialog.close()

    def redraw_board(self):  # redraws the board after updates to the logical board
        self.board.update()

    def end_game(self):
        # stop the timers and the animation of the labels
        GameLogic.player1["timer"].stop()
        GameLogic.player2["timer"].stop()
        self.p1_side.stop_turn_animation()
        self.p2_side.stop_turn_animation()

        end_dialog = GameEndDialog(
            self.reset_game, self.back_to_start_signal
        )  # show the game end dialog that shows the scores and allows player to start a new game or a rematch
        self.help_dialog.close()
        end_dialog.exec()

    def switch_timers(
        self,
    ):  # start a timer and stops the other one based on which player is the current player and it also switches which turn_label is animated
        if GameLogic.current_player == GameLogic.player1:
            if self.is_speed_go:
                GameLogic.player1[
                    "timer"
                ].start()  # start the timer and animation for player 1
                GameLogic.player2["timer"].stop()
            self.p1_side.start_turn_animation()
            self.p2_side.stop_turn_animation()

        else:
            if self.is_speed_go:
                GameLogic.player2[
                    "timer"
                ].start()  # start the timer and animation  for player 2
                GameLogic.player1["timer"].stop()
            self.p2_side.start_turn_animation()
            self.p1_side.stop_turn_animation()

    def pause_game(self):
        GameLogic.player2["timer"].stop()  # stop both timers
        GameLogic.player1["timer"].stop()
        pause_dialog = PauseDialog()  # show a pause dialog
        pause_dialog.exec()
        GameLogic.current_player[
            "timer"
        ].start()  # afte the dialog is executed we continue with the timer

    def instruction_widget(self):
        self.help_dialog.show()  # show the game rules widget

    def open_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec()
