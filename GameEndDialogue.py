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


class GameEndDialog(QDialog):
    def __init__(
        self,
        player1,
        player2,
    ):  # takes all the palyer info
        super().__init__()

        self.player1 = player1
        self.player2 = player2

        # set the main window stuff
        self.setWindowTitle("Game Over")
        self.setStyleSheet("background-color: #141414;")
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
        quit_button = PrimaryButton("Quit", self.quit_application)

        # ad the widgets to the main layout
        layout.addWidget(label, 0, 0, 1, 2)
        icon = QIcon("images/trophy.png")  # show the medal icon as well
        medal_image = QLabel()
        medal_image.setPixmap(icon.pixmap(100, 100))
        medal_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(medal_image, 1, 0, 1, 2)  # add the medal icon
        self.setFixedHeight(350)  # update overall size of dialog
        label.setFixedHeight(105)
        label.setStyleSheet("QLabel { line-height: 0px;color:white; }")
        layout.addWidget(quit_button, 2, 0, 1, 2)
        layout.update()  # to make sure empty rows are squshed

    def set_winner_text(self, label):  # sets text based on which player won the game or if its a draw , it will show that
        p1_score = self.player1["score"][0] + self.player1["score"][1] 
        p2_score = self.player2["score"][0] + self.player2["score"][1] 

        if p1_score > p2_score:
            winner_name = self.player1["name"]
        else:
            winner_name = self.player2["name"]
        
        label.setText(winner_name + "\nwins the game!")

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
        
    def quit_application(self):
        QApplication.quit()
