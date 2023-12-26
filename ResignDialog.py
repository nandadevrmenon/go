from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QGridLayout,
)
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from PrimaryButton import PrimaryButton
from PyQt6.QtCore import Qt
from PyQt6 import QtCore


class GameEndDialog(QDialog):
    def __init__(
        self,
        player1,
        p1_score,
        player2,
        p2_score,
        mode,
        rematch_callback,
        start_screen_callback,
    ):  # takes all the palyer info, callback for rematch and callback for staring the screen again
        super().__init__()

        self.player1 = player1
        self.player2 = player2
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.mode = mode
        self.start_screen_callback = start_screen_callback
        self.rematch_callback = rematch_callback

        # set the main window stuff
        self.setWindowTitle("Game Over")
        self.setStyleSheet("background-color: #070114;")
        self.setFixedHeight(200)
        self.setFixedWidth(300)

        # main grid layout
        layout = QGridLayout(self)

        label = QLabel("")  # main lable
        self.set_winner_text(label)  # adds  the name of the winner to the label
        label.setFont(QFont(self.get_statliches(), 35))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white;")
        label.setFixedHeight(30)

        points_label = QLabel("")
        self.set_points_text(
            points_label
        )  # sets the point difference between two player or it show that
        points_label.setFont(QFont(self.get_josefin(), 18))
        points_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        points_label.setStyleSheet("color: white;")
        points_label.setFixedHeight(30)

        rematch_button = PrimaryButton("Rematch", self.rematch)
        new_game_button = PrimaryButton("New Game", self.new_game)

        # ad the widgets to the main layout
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(points_label, 1, 0, 1, 2)
        layout.addWidget(rematch_button, 3, 0, 1, 1)
        layout.addWidget(new_game_button, 3, 1, 1, 1)

        if not self.p1_score == self.p2_score:  # if not a draw
            icon = QIcon("icons/medal.png")  # show the medal icon as well
            medal_image = QLabel()
            medal_image.setPixmap(icon.pixmap(100, 100))
            medal_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(medal_image, 2, 0, 1, 2)  # add the medal icon
            self.setFixedHeight(350)  # update overall size of dialog
            label.setFixedHeight(75)
            label.setStyleSheet("QLabel { line-height: 0px;color:white; }")

        layout.update()  # to make sure empty rows are squshed

    def rematch(
        self,
    ):  # call the rematch  callback which called the function in the sidebar component
        self.close()
        self.rematch_callback()

    def new_game(
        self,
    ):  # calls afunction that emits our custom signal which shows the strt screen again so different players can start a new game
        self.close()
        self.start_screen_callback.emit()

    def set_winner_text(
        self, label
    ):  # sets text based on which player won the game or if its a draw , it will show that
        if self.p1_score > self.p2_score:
            label.setText(self.player1 + "\nwins the game!")
        elif self.p2_score > self.p1_score:
            label.setText(self.player2 + "\nwins the game!")
        else:
            label.setText("Its a draw.")

    def set_points_text(
        self, label
    ):  # will calulate the point difference between the players and set the text of the label to show the difference
        if self.p1_score == self.p2_score:
            label.setText("You both have " + str(self.p1_score) + " points")
        else:
            diff = abs(self.p1_score - self.p2_score)
            label.setText("by " + str(diff) + " points")

    def get_statliches(self):  # to get the font from the file
        font_path = QtCore.QDir.currentPath() + "/fonts/statliches.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        # Check if the font was loaded successfully
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            print("font not found ")
            return "Helvetica"

    def get_josefin(self):  # to get the font from the file
        font_path = QtCore.QDir.currentPath() + "/fonts/josefin.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        # Check if the font was loaded successfully
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            print("font not found ")
            return "Helvetica"
