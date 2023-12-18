from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QGridLayout,
    QButtonGroup,
    QRadioButton,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PrimaryButton import PrimaryButton
from SecondaryButton import SecondaryButton
from PyQt6 import QtCore
from PyQt6 import QtCore
from PyQt6.QtGui import QFontDatabase

from styles import colors


# from QuitDialog import QuitDialog


class StartScreen(QMainWindow):
    from styles import colors

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # set up the main user interface
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {colors['light black']};")
        self.setCentralWidget(central_widget)
        main_grid_layout = QGridLayout(central_widget)
        main_grid_layout.setContentsMargins(40, 40, 40, 40)
        self.setFixedHeight(350)
        self.setFixedWidth(350)

        # Logo
        main_logo_widget = QWidget()
        main_logo_layout = QVBoxLayout()

        main_logo_label = QLabel("Go")
        main_logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_font = QFont(get_tan_nimbus(), 70)
        main_logo_label.setFont(logo_font)
        main_logo_label.setStyleSheet(f"color:{colors['yellow']}")
        main_logo_label.setFixedHeight(70)

        main_logo_subtext = QLabel("The 2 player strategy game")
        main_logo_subtext.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtext_font = QFont(get_statliches(), 20)
        main_logo_subtext.setFont(subtext_font)
        main_logo_subtext.setStyleSheet(f"color:{colors['yellow']}")
        main_logo_subtext.setFixedHeight(20)

        main_logo_layout.addWidget(main_logo_label)
        main_logo_layout.addWidget(main_logo_subtext)
        main_logo_layout.setContentsMargins(0, 0, 0, 0)
        main_logo_widget.setLayout(main_logo_layout)

        # Form with labels and text boxes
        player1_label = QLabel("Player 1:")
        player1_label.setStyleSheet("color:white;")  # white text

        self.player1_name = QLineEdit()
        self.player1_name.setPlaceholderText("Nickname")  # set placeholder text
        self.player1_name.setStyleSheet(
            f"background-color: {colors['lighter black']}; color: #ffffff;"
        )  # set dark purple bg and set color to white

        # same as above
        player2_label = QLabel("Player 2:")
        player2_label.setStyleSheet("color:white")

        self.player2_name = QLineEdit()
        self.player2_name.setPlaceholderText("Nickname")
        self.player2_name.setStyleSheet(
            f"background-color: {colors['lighter black']}; color: #ffffff;"
        )

        # two primary buttons one to start game and the other to quit
        submit_button = PrimaryButton("Start Game", lambda x: x + 1)
        quit_button = SecondaryButton("Quit Game", lambda x: x + 1)

        # Add widgets to the layout
        main_grid_layout.addWidget(main_logo_widget, 0, 0, 6, 5)
        main_grid_layout.addWidget(player1_label, 6, 0, 1, 1)
        main_grid_layout.addWidget(self.player1_name, 6, 1, 1, 4)
        main_grid_layout.addWidget(player2_label, 7, 0, 1, 1)
        main_grid_layout.addWidget(self.player2_name, 7, 1, 1, 4)
        main_grid_layout.addWidget(submit_button, 8, 0, 1, 5)
        main_grid_layout.addWidget(quit_button, 9, 0, 1, 5)


def get_tan_nimbus():  # gets the font used for tehe logo of the app
    # all fonts from fonts.google.com
    font_path = QtCore.QDir.currentPath() + "/fonts/press.ttf"
    font_id = QFontDatabase.addApplicationFont(font_path)
    # Check if the font was loaded successfully
    if font_id != -1:
        return QFontDatabase.applicationFontFamilies(font_id)[0]
    else:
        return "Helvetica"


def get_statliches():  # gets the font used for tehe logo of the app
    # all fonts from fonts.google.com
    font_path = QtCore.QDir.currentPath() + "/fonts/statliches.ttf"
    font_id = QFontDatabase.addApplicationFont(font_path)
    # Check if the font was loaded successfully
    if font_id != -1:
        return QFontDatabase.applicationFontFamilies(font_id)[0]
    else:
        return "Helvetica"
