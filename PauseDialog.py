from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QGridLayout,
)
from PyQt6.QtGui import QIcon, QFont
from SecondaryButton import SecondaryButton
from PrimaryButton import PrimaryButton
from PyQt6.QtCore import Qt
from styles import colors


class PauseDialog(QDialog):  # a dialog that just shows that the game is paused
    def __init__(
        self,
    ):
        super().__init__()
        self.setWindowTitle("Game has been paused")
        self.setStyleSheet(f"background-color: {colors['light black']};")
        self.setMinimumHeight(230)
        self.setMinimumWidth(230)
        self.setMaximumHeight(300)
        self.setMaximumWidth(300)

        layout = QGridLayout(self)

        label = QLabel("Game Paused")
        label.setFont(QFont("Helvetica", 18))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white;")
        label.setFixedHeight(20)

        icon_label = QLabel()
        icon_label.setPixmap(
            QIcon("images/pause.png").pixmap(100, 100)
        )  # shows a sad panda
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yes_button = PrimaryButton(
            "Resume", self.close_dialog
        )  # secondary button that quit application

        # add all the widgets
        layout.addWidget(label, 0, 0, 1, 5)
        layout.addWidget(icon_label, 1, 0, 2, 5)
        layout.addWidget(yes_button, 3, 1, 1, 3)

    def close_dialog(self):
        self.close()
