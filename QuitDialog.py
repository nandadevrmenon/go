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


class QuitDialog(QDialog):
    def __init__(
        self,
    ):
        super().__init__()
        self.setWindowTitle("Confirmation")
        self.setStyleSheet("background-color: #070114;")

        layout = QGridLayout(self)

        label = QLabel("Are you sure you want to quit?")
        label.setFont(QFont("Helvetica", 18))
        label.setStyleSheet("color: white;")

        icon_label = QLabel()
        icon_label.setPixmap(
            QIcon("icons/sad.png").pixmap(100, 100)
        )  # shows a sad panda
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yes_button = SecondaryButton(
            "Yes", self.quit_application
        )  # secondary button that quit application

        no_button = PrimaryButton(
            "No", self.close_dialog
        )  # primary button that closes the confomraiton dialog

        # add all the widgets
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(icon_label, 1, 0, 1, 2)
        layout.addWidget(yes_button, 2, 0, 1, 1)
        layout.addWidget(no_button, 2, 1, 1, 1)

    def quit_application(self):
        QApplication.quit()

    def close_dialog(self):
        self.close()
