from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QApplication,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QFontDatabase
from PrimaryButton import PrimaryButton
from SecondaryButton import SecondaryButton
from styles import colors

# from WarningButton import WarningButton
# from GameEndDialogue import GameEndDialog
# from SkipTurnDialog import SkipTurnDialog
# from CorrectGuessDialog import CorrectGuessDialog
import random, csv
import sys


class SideBar(QWidget):
    def __init__(self, player, has_kumi, starts_first=False):
        super().__init__()

        # main components settings
        main_vbox = QVBoxLayout()  # main vertical layout
        self.setStyleSheet("QWidget{background-color:#141414;}")
        self.setLayout(main_vbox)
        self.setContentsMargins(0, 0, 0, 0)
        main_vbox.setContentsMargins(20, 30, 20, 0)
        main_vbox.setSpacing(20)
        self.setMinimumWidth(260)
        self.setMaximumWidth(280)

        # initialise the fonts
        statliches = self.get_statliches_font()
        statliches_heading1 = QFont(statliches, 35)  # minimalist display font
        statliches_heading2 = QFont(statliches, 25)
        statliches_heading3 = QFont(statliches, 20)
        statliches_body = QFont(statliches, 16)
        font_color_white = f"color:{colors['white']}"
        align_left = Qt.AlignmentFlag.AlignLeft
        align_right = Qt.AlignmentFlag.AlignRight
        align_center = Qt.AlignmentFlag.AlignCenter

        # game variables
        self.player = player
        self.has_kumi = has_kumi
        self.kumi = 7.5 if self.has_kumi else 0
        self.starts_first = starts_first
        self.player_name = str(player["name"]).upper()
        territory = player["score"][0]
        captured = player["score"][1]

        self.timer = player["timer"]  # to time the rounds
        self.timer_counter = 120
        self.timer.setInterval(1000)
        self.timer.timeout.connect(
            self.update_timer
        )  # after every 1 second(which is the timeout for this one) we update the timer label

        player_box = QWidget()

        # layout for the turn_tox
        player_box_grid = QGridLayout()
        player_box.setLayout(player_box_grid)
        player_box.setObjectName("player_box")
        player_box.setStyleSheet(
            "QWidget#player_box {border: 1px solid #171717; border-radius:10px; background-color:#262626;} QLabel {background-color:#262626;}"
        )

        # indicates which player's turn it is to draw
        self.turn_label = QLabel("It's your turn!")
        self.turn_label.setFont(statliches_heading1)
        self.turn_label.setAlignment(align_center)
        self.turn_label.setStyleSheet(
            f"color:{colors['grey']};"
            if not self.starts_first
            else f"color:{colors['orange']};"
        )
        self.turn_label.setMinimumHeight(40)
        self.animate_text_timer = QTimer(
            self
        )  # connects a timer for the color change intevals
        self.animate_text_timer.setInterval(600)
        self.animate_text_timer.timeout.connect(self.animate_turn_text)
        self.colorFlag = not self.starts_first

        # label for player information
        self.player_label = QLabel(self.player_name)
        self.player_label.setFont(statliches_heading1)
        self.player_label.setAlignment(align_left)
        self.player_label.setStyleSheet(f"color:{colors['yellow']}")
        color_label = QLabel("White" if self.has_kumi else "Black")
        color_label.setFont(statliches_heading2)
        color_label.setStyleSheet(font_color_white)
        color_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter
        )

        # shows the time remaining and is being updated by the QTimer
        self.timer_label = QLabel("02 : 00")
        self.timer_label.setFont(statliches_heading2)
        self.timer_label.setAlignment(align_right if self.has_kumi else align_left)

        # add everything to the turnbox vertical layout
        player_box_grid.addWidget(self.turn_label, 0, 0, 1, 2)
        player_box_grid.addWidget(self.player_label, 1, 0, 1, 1)
        player_box_grid.addWidget(color_label, 1, 1, 1, 1)
        player_box_grid.addWidget(self.timer_label, 2, 0, 1, 2)
        player_box.setMinimumHeight(170)

        # the box with the scores
        score_box = QWidget()

        # set up the layout for the score box
        score_grid = QGridLayout()
        score_box.setLayout(score_grid)
        score_box.setContentsMargins(0, 0, 0, 20)

        # score heading
        self.total_label = QLabel("SCORE : " + str(territory + captured + self.kumi))
        self.total_label.setFont(statliches_heading1)
        self.total_label.setAlignment(align_right if self.has_kumi else align_left)
        self.total_label.setStyleSheet(font_color_white)
        self.total_label.setContentsMargins(0, 5, 0, 10)

        # player 1's name
        territory_label = QLabel("Territory")
        territory_label.setFont(statliches_heading3)
        territory_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        territory_label.setStyleSheet(font_color_white)

        # player 1's score
        self.territory_value = QLabel(str(territory))
        self.territory_value.setFont(statliches_heading3)
        self.territory_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.territory_value.setStyleSheet(font_color_white)

        # pieces captures label
        captured_label = QLabel("Captured")
        captured_label.setFont(statliches_heading3)
        captured_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        captured_label.setStyleSheet(font_color_white)

        # player 2's score
        self.captured_value = QLabel(str(captured))
        self.captured_value.setFont(statliches_heading3)
        self.captured_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.captured_value.setStyleSheet(font_color_white)

        # kumi
        kumi_label = QLabel("Kumi")
        kumi_label.setFont(statliches_heading3)
        kumi_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        kumi_label.setStyleSheet(font_color_white)

        # kumi score addition if applicable
        self.kumi_value = QLabel(str(self.kumi))
        self.kumi_value.setFont(statliches_heading3)
        self.kumi_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.kumi_value.setStyleSheet(font_color_white)

        # add all the widgets created above to the score_grid layout
        if self.has_kumi:
            score_grid.addWidget(self.total_label, 0, 0, 1, 5)
            score_grid.addWidget(territory_label, 1, 2, 1, 1)
            score_grid.addWidget(self.territory_value, 1, 4, 1, 1)
            score_grid.addWidget(captured_label, 2, 2, 1, 1)
            score_grid.addWidget(self.captured_value, 2, 4, 1, 1)
            score_grid.addWidget(kumi_label, 3, 2, 1, 1)
            score_grid.addWidget(self.kumi_value, 3, 4, 1, 1)
        else:
            score_grid.addWidget(self.total_label, 0, 0, 1, 5)
            score_grid.addWidget(territory_label, 1, 0, 1, 1)
            score_grid.addWidget(self.territory_value, 1, 2, 1, 1)
            score_grid.addWidget(captured_label, 2, 0, 1, 1)
            score_grid.addWidget(self.captured_value, 2, 2, 1, 1)
            score_grid.addWidget(kumi_label, 3, 0, 1, 1)
            score_grid.addWidget(self.kumi_value, 3, 2, 1, 1)

        spacer = (
            QSpacerItem(  # spacer between the last row of 2 buttons and everything else
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # adds the three boxes to the main widget
        main_vbox.addWidget(player_box)
        main_vbox.addWidget(score_box)
        main_vbox.addItem(spacer)

    def update_score(self):
        territory = self.player["score"][0]
        captured = self.player["score"][1]

        self.total_label.setText("SCORE : " + str(territory + captured + self.kumi))
        self.territory_value.setText(str(territory))
        self.captured_value.setText(str(captured))

    def update_timer(self):
        # Update the countdown and display
        self.timer_counter -= 1

        if self.timer_counter < 0:
            # Stop the timer when the countdown reaches 0
            self.timer.stop()
            return

        # Convert remaining seconds to minutes and seconds
        minutes = self.timer_counter // 60
        seconds = self.timer_counter % 60

        # Display the countdown in the label
        self.timer_label.setText(f"{minutes:02} : {seconds:02}")

    def stop_turn_animation(self):
        self.animate_text_timer.stop()
        self.turn_label.setStyleSheet(f"color:{colors['grey']}; ")
        self.colorFlag = True

    def start_turn_animation(self):
        self.turn_label.setStyleSheet(f"color:{colors['orange']}; ")
        self.colorFlag = False
        self.animate_text_timer.start()

    def default_turn_animation(self):
        self.animate_text_timer.stop()
        self.turn_label.setStyleSheet(
            f"color:{colors['grey']};"
            if not self.starts_first
            else f"color:{colors['orange']};"
        )
        self.colorFlag = not self.starts_first

    def reset_timer(self):
        self.timer.stop()
        self.timer_counter = 120
        self.timer_label.setText("02 : 00")

    def get_press2p_font(self):
        font_path = QtCore.QDir.currentPath() + "/fonts/press.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)  # load font
        # Check if the font was loaded successfully
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            return "Helvetica"  # fallback

    def get_josefin(self):
        font_path = QtCore.QDir.currentPath() + "/fonts/josefin.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)  # lond font
        # Check if the font was loaded successfully
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            return "Helvetica"  # fallback

    def get_statliches_font(self):
        font_path = QtCore.QDir.currentPath() + "/fonts/statliches.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)  # load font
        # Check if the font was loaded successfully
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            return "Helvetica"  # fallback

    def animate_turn_text(self):
        """
        sets the color to orange when color flag is true; white when false.
        connected to a timer interval, it will create a "flashing" effect
        """
        if self.colorFlag:
            self.turn_label.setStyleSheet(f"color:{colors['orange']};")
        else:
            self.turn_label.setStyleSheet(f"color:{colors['grey']}; ")
        self.colorFlag = not self.colorFlag


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SideBar(
        {"name": "asd", "score": [0, 0], "timer": QTimer()}, True
    )  # open the start screen of the game
    window.show()
    app.exec()  # start the event loop running
