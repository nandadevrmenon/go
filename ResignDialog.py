from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QGridLayout,
)
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from PrimaryButton import PrimaryButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6 import QtCore
from SecondaryButton import SecondaryButton
from styles import colors
from game_logic import GameLogic


class ResignDialog(QDialog):
    def __init__(
        self,
        rematch_callback,
        start_screen_callback,
    ):  # takes all the palyer info, callback for rematch and callback for staring the screen again
        super().__init__()
        self.rematch_callback = rematch_callback
        self.start_screen_callback = start_screen_callback

        self.setWindowTitle("")
        self.setStyleSheet(f"background-color: {colors['light black']};")

        layout = QGridLayout(self)

        player_name = GameLogic.current_player["name"]
        label = QLabel(player_name + " lost the game")
        label.setFont(QFont(self.get_statliches(), 18))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel()
        icon_label.setPixmap(
            QIcon("images/end.png").pixmap(100, 100)
        )  # shows a sad panda
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yes_button = SecondaryButton(
            "Rematch", self.rematch
        )  # secondary button that quit application

        no_button = PrimaryButton(
            "New Game", self.new_game
        )  # primary button that closes the confomraiton dialog

        # add all the widgets
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(icon_label, 1, 0, 1, 2)
        layout.addWidget(yes_button, 2, 0, 1, 1)
        layout.addWidget(no_button, 2, 1, 1, 1)

    def rematch(
        self,
    ):  # call the rematch  callback which called the function in the sidebar component
        self.rematch_callback()
        self.close()

    def new_game(
        self,
    ):  # calls afunction that emits our custom signal which shows the strt screen again so different players can start a new game
        self.close()
        self.start_screen_callback.emit()
        # self.start_screen_callback.emit()

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
