from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLabel,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QFontDatabase
from styles import colors


# SideBar class provides a widget for displaying player information and game scores
class SideBar(QWidget):
    def __init__(
        self,
        player,
        has_kumi,
        starts_first=False,
        is_speed_go=False,
        resign_callback=None,
    ):
        # Call the constructor of the parent class (QWidget)
        super().__init__()

        # Create a main vertical layout for the SideBar
        main_vbox = QVBoxLayout()
        self.setStyleSheet("QWidget{background-color:#141414;}")
        self.setLayout(main_vbox)
        self.setContentsMargins(0, 0, 0, 0)
        main_vbox.setContentsMargins(20, 30, 20, 0)
        main_vbox.setSpacing(20)
        self.setMinimumWidth(260)
        self.setMaximumWidth(280)

        # Initialize fonts
        statliches = self.get_statliches_font()
        statliches_heading1 = QFont(statliches, 35)  # Minimalist display font
        statliches_heading2 = QFont(statliches, 25)
        statliches_heading3 = QFont(statliches, 20)

        font_color_white = f"color:{colors['white']}"
        align_left = Qt.AlignmentFlag.AlignLeft
        align_right = Qt.AlignmentFlag.AlignRight
        align_center = Qt.AlignmentFlag.AlignCenter

        # Game variables
        self.resign_callback = resign_callback
        self.player = player
        self.has_kumi = has_kumi
        self.kumi = 7.5 if self.has_kumi else 0
        self.starts_first = starts_first
        self.player_name = str(player["name"]).upper()
        self.is_speed_go = is_speed_go
        territory = player["score"][0]
        captured = player["score"][1]

        if self.is_speed_go:
            self.timer = player["timer"]  # Timer to track rounds
            self.timer_counter = 120
            self.timer.setInterval(1)
            self.timer.timeout.connect(
                self.update_timer
            )  # Connect timeout to update_timer method

        # Create a QWidget for player information
        player_box = QWidget()

        # Create a grid layout for the player_box
        player_box_grid = QGridLayout()
        player_box.setLayout(player_box_grid)
        player_box.setObjectName("player_box")
        player_box.setStyleSheet(
            "QWidget#player_box {border: 1px solid #171717; border-radius:10px; background-color:#262626;} QLabel {background-color:#262626;}"
        )

        # Label to indicate player's turn
        self.turn_label = QLabel("It's your turn!")
        self.turn_label.setFont(statliches_heading2)
        self.turn_label.setAlignment(align_center)
        self.turn_label.setStyleSheet(
            f"color:{colors['grey']};"
            if not self.starts_first
            else f"color:{colors['orange']};"
        )
        self.animate_text_timer = QTimer(self)  # Timer for color change intervals
        self.animate_text_timer.setInterval(600)
        self.animate_text_timer.timeout.connect(self.animate_turn_text)
        self.colorFlag = not self.starts_first

        # Label for player information
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

        # Label to display remaining time (for speed go)
        self.timer_label = QLabel("02 : 00")
        self.timer_label.setFont(statliches_heading2)
        self.timer_label.setAlignment(align_right if self.has_kumi else align_left)

        # Add widgets to player_box layout
        player_box_grid.addWidget(self.turn_label, 0, 0, 1, 2)
        player_box_grid.addWidget(self.player_label, 1, 0, 1, 1)
        player_box_grid.addWidget(color_label, 1, 1, 1, 1)
        if self.is_speed_go:
            player_box_grid.addWidget(self.timer_label, 2, 0, 1, 2)
        player_box.setMinimumHeight(120 if self.is_speed_go else 80)

        # Create a QWidget for displaying scores
        score_box = QWidget()

        # Set up a grid layout for the score_box
        score_grid = QGridLayout()
        score_box.setLayout(score_grid)
        score_box.setContentsMargins(0, 0, 0, 20)

        # Label to display total score
        self.total_label = QLabel("SCORE : " + str(territory + captured + self.kumi))
        self.total_label.setFont(statliches_heading1)
        self.total_label.setAlignment(align_right if self.has_kumi else align_left)
        self.total_label.setStyleSheet(font_color_white)
        self.total_label.setContentsMargins(0, 5, 0, 10)

        # Label and value for stones (territory)
        territory_label = QLabel("Stones")
        territory_label.setFont(statliches_heading3)
        territory_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        territory_label.setStyleSheet(font_color_white)

        self.territory_value = QLabel(str(territory))
        self.territory_value.setFont(statliches_heading3)
        self.territory_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.territory_value.setStyleSheet(font_color_white)

        # Label and value for captured pieces
        captured_label = QLabel("Captured")
        captured_label.setFont(statliches_heading3)
        captured_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        captured_label.setStyleSheet(font_color_white)

        self.captured_value = QLabel(str(captured))
        self.captured_value.setFont(statliches_heading3)
        self.captured_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.captured_value.setStyleSheet(font_color_white)

        # Label and value for Kumi (if applicable)
        kumi_label = QLabel("Kumi")
        kumi_label.setFont(statliches_heading3)
        kumi_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        kumi_label.setStyleSheet(font_color_white)

        self.kumi_value = QLabel(str(self.kumi))
        self.kumi_value.setFont(statliches_heading3)
        self.kumi_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.kumi_value.setStyleSheet(font_color_white)

        # Add score widgets to score_grid layout
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

        # Spacer item
        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        # Add player_box, score_box, and spacer to the main layout
        main_vbox.addWidget(player_box)
        main_vbox.addWidget(score_box)
        main_vbox.addItem(spacer)

    # Method to update scores
    def update_score(self):
        territory = self.player["score"][0]
        captured = self.player["score"][1]

        self.total_label.setText("SCORE : " + str(territory + captured + self.kumi))
        self.territory_value.setText(str(territory))
        self.captured_value.setText(str(captured))

    # Method to update the timer (if applicable)
    def update_timer(self):
        self.timer_counter -= 0.001

        if self.timer_counter < 0:
            self.timer.stop()
            self.resign_callback()
            return

        minutes = self.timer_counter // 60
        seconds = self.timer_counter % 60

        self.timer_label.setText(f"{int(minutes):02} : {int(seconds):02}")

    # Method to stop the turn animation
    def stop_turn_animation(self):
        self.animate_text_timer.stop()
        self.turn_label.setStyleSheet(f"color:{colors['grey']}; ")
        self.colorFlag = True

    # Method to start the turn animation
    def start_turn_animation(self):
        self.turn_label.setStyleSheet(f"color:{colors['orange']}; ")
        self.colorFlag = False
        self.animate_text_timer.start()

    # Method to set default turn animation
    def default_turn_animation(self):
        self.animate_text_timer.stop()
        self.turn_label.setStyleSheet(
            f"color:{colors['grey']};"
            if not self.starts_first
            else f"color:{colors['orange']};"
        )
        self.colorFlag = not self.starts_first

    # Method to reset the timer
    def reset_timer(self):
        self.timer.stop()
        self.timer_counter = 120
        self.timer_label.setText("02 : 00")

    # Method to get the Press2P font
    def get_press2p_font(self):
        font_path = QtCore.QDir.currentPath() + "/fonts/press.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            return "Helvetica"

    # Method to get the Josefin font
    def get_josefin(self):
        font_path = QtCore.QDir.currentPath() + "/fonts/josefin.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            return "Helvetica"

    # Method to get the Statliches font
    def get_statliches_font(self):
        font_path = QtCore.QDir.currentPath() + "/fonts/statliches.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            return "Helvetica"

    # Method to animate the turn text for a flashing effect
    def animate_turn_text(self):
        if self.colorFlag:
            self.turn_label.setStyleSheet(f"color:{colors['orange']};")
        else:
            self.turn_label.setStyleSheet(f"color:{colors['grey']}; ")
        self.colorFlag = not self.colorFlag
