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


class QuitDialog(QDialog):
    def __init__(
        self,
    ):
        super().__init__()
        self.setWindowTitle("Confirmation")
        self.setStyleSheet(f"background-color: {colors['light black']};")

        layout = QGridLayout(self)

        label = QLabel("Are you sure you want to quit?")
        label.setFont(QFont("Helvetica", 18))
        label.setStyleSheet("color: white;")

        yes_button = SecondaryButton(
            "Yes", self.quit_application
        )  # secondary button that quit application

        no_button = PrimaryButton(
            "No", self.close_dialog
        )  # primary button that closes the confomraiton dialog

        # add all the widgets
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0, 1, 1)
        layout.addWidget(no_button, 1, 1, 1, 1)

    def quit_application(self):
        QApplication.quit()

    def close_dialog(self):
        self.close()
