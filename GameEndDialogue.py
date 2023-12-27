from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QGridLayout,
)
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from PrimaryButton import PrimaryButton
from PyQt6.QtCore import Qt
from PyQt6 import QtCore

from game_logic import GameLogic


class GameEndDialog(QDialog):
    def __init__(
        self, rematch_callback, back_to_start_signal
    ):  # takes all the palyer info
        super().__init__()
        self.rematch_callback = rematch_callback
        self.back_to_start_signal = back_to_start_signal
        self.player1 = GameLogic.player1
        self.player2 = GameLogic.player2

        # set the main window stuff
        self.setWindowTitle("Game Over")
        self.setStyleSheet("background-color: #141414;")
        self.setFixedWidth(400)

        # main grid layout
        layout = QGridLayout(self)

        label = QLabel("")  # main lable
        self.set_winner_text(label)  # adds  the name of the winner to the label
        label.setFont(QFont(self.get_statliches(), 35))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white;")

        score_label = QLabel("")  # sec lable
        score_label.setFont(QFont(self.get_statliches(), 20))
        score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_label.setStyleSheet("color: white;")

        self.opponent_score_label = QLabel()
        self.opponent_score_label.setFont(QFont(self.get_statliches(), 20))
        self.opponent_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.opponent_score_label.setStyleSheet("color: white;")

        self.set_score_text(score_label)  # adds  the name of the winner to the label

        rematch_button = PrimaryButton("Rematch", self.rematch)
        new_game_button = PrimaryButton("New Game", self.new_game)

        # ad the widgets to the main layout
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(score_label, 1, 0, 2, 2)
        icon = QIcon("images/trophy.png")  # show the medal icon as well
        medal_image = QLabel()
        medal_image.setPixmap(icon.pixmap(100, 100))
        medal_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(medal_image, 3, 0, 1, 2)  # add the medal icon
        label.setStyleSheet("QLabel { line-height: 0px;color:white; }")
        layout.addWidget(self.opponent_score_label, 4, 0, 1, 2)
        layout.addWidget(rematch_button, 5, 0, 1, 1)
        layout.addWidget(new_game_button, 5, 1, 1, 1)
        layout.update()  # to make sure empty rows are squshed

    def set_winner_text(
        self, label
    ):  # sets text based on which player won the game or if its a draw , it will show that
        p1_score, p2_score = self.get_end_score()

        if p1_score > p2_score:
            winner_name = self.player1["name"]
        else:
            winner_name = self.player2["name"]

        label.setText(winner_name + "\nwins the game!")

    def get_end_score(self):  # get end score
        p1_territory, p2_territory = GameLogic.calculate_territories()

        p1_score = (
            self.player1["score"][0] + self.player1["score"][1] + p1_territory
        )  # stones on board + territories
        p2_score = (
            self.player2["score"][0] + self.player2["score"][1] + p2_territory + 7.5
        )  # 7.5 kumi for white player

        return p1_score, p2_score

    def set_score_text(
        self, score_label
    ):  # sets text based on which player won the game or if its a draw , it will show that
        p1_score, p2_score = self.get_end_score()
        p1_territory, p2_territory = GameLogic.calculate_territories()

        if p1_score > p2_score:
            stone = self.player1["score"][0]
            captured = self.player1["score"][1]
            territory = p1_territory
            total_score = p1_score
            self.opponent_score_label.setText(
                self.player2["name"] + " only had " + str(p2_score) + " points."
            )
        else:
            stone = self.player2["score"][0]
            captured = self.player2["score"][1]
            territory = p2_territory
            total_score = p2_score
            self.opponent_score_label.setText(
                self.player1["name"] + " only had " + str(p1_score) + " points."
            )

        score_label.setText(
            "Stones: "
            + str(stone)
            + "\nCaptured: "
            + str(captured)
            + "\nTerritories: "
            + str(territory)
            + "\n Total: "
            + str(total_score)
        )

    def rematch(self):
        self.close()
        self.rematch_callback()

    def new_game(self):
        self.close()
        self.back_to_start_signal.emit()

    def get_statliches(self):  # to get the font from the file
        font_path = QtCore.QDir.currentPath() + "/fonts/statliches.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        # Check if the font was loaded successfully
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            print("font not found ")
            return "Helvetica"
