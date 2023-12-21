from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QGridLayout,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PrimaryButton import PrimaryButton
from SecondaryButton import SecondaryButton
from PyQt6 import QtCore
from PyQt6 import QtCore
from PyQt6.QtGui import QFontDatabase
from QuitDialog import QuitDialog
from GameScreen import GameScreen
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
        submit_button = PrimaryButton("Start Game", self.show_game_screen)
        quit_button = SecondaryButton("Quit Game", self.show_quit_confirmation)

        # Add widgets to the layout
        main_grid_layout.addWidget(main_logo_widget, 0, 0, 6, 5)
        main_grid_layout.addWidget(player1_label, 6, 0, 1, 1)
        main_grid_layout.addWidget(self.player1_name, 6, 1, 1, 4)
        main_grid_layout.addWidget(player2_label, 7, 0, 1, 1)
        main_grid_layout.addWidget(self.player2_name, 7, 1, 1, 4)
        main_grid_layout.addWidget(submit_button, 8, 0, 1, 5)
        main_grid_layout.addWidget(quit_button, 9, 0, 1, 5)

    def show_game_screen(self):
        player1 = self.player1_name.text()  # get the names of the two players
        player2 = self.player2_name.text()

        # validate the names and produce an error message
        player1_valid, error_msg1 = self.validate_player_name(player1)
        player2_valid, error_msg2 = self.validate_player_name(player2)

        if player1_valid and player2_valid:
            self.game_screen = GameScreen(
                player1, player2
            )  # we create a new game screen with the player names and the mode
            self.game_screen.back_to_start_signal.connect(
                self.show_start_screen
            )  # this is a custom signal fromt he game screen that opens the startscreen again withtou using circular imports
            self.game_screen.show()  # show the game screen
            self.close()  # close the start screen
        else:
            if not player1_valid:  # is any name is not valid
                self.player1_name.clear()  # we clear that input
                self.player1_name.setPlaceholderText(
                    error_msg1
                )  # and show the error message as place holder text
            if not player2_valid:
                self.player2_name.clear()
                self.player2_name.setPlaceholderText(error_msg2)

    def show_start_screen(self):
        self.player1_name.clear()  # we clear the inputs
        self.player2_name.clear()
        self.game_screen.close()  # close the game screen
        self.show()  # and re open the start screen

    def show_quit_confirmation(self):
        dialog = QuitDialog()  # show the confirm quit dialog
        dialog.exec()

    def validate_player_name(self, name):
        # Minimum and maximum length check
        if len(name) < 2:
            return False, "Name must be longer"

        if len(name) > 10:
            return False, "Name must be shorter"

        # onyl alphanumeric and spaces allowed
        if not name.isalnum() or not name.replace(" ", "").isalnum():
            return False, "Name must be alphanumeric"

        # else
        return True, ""


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
