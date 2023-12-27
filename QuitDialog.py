from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QGridLayout
from PyQt6.QtGui import QIcon, QFont
from SecondaryButton import SecondaryButton
from PrimaryButton import PrimaryButton
from PyQt6.QtCore import Qt
from styles import colors


# Define a custom QuitDialog class that inherits from QDialog
class QuitDialog(QDialog):
    def __init__(
        self,
    ):
        # Call the constructor of the parent class (QDialog)
        super().__init__()

        # Set the window title and background color
        self.setWindowTitle("Confirmation")
        self.setStyleSheet(f"background-color: {colors['light black']};")

        # Create a layout for the dialog
        layout = QGridLayout(self)

        # Create a label with the confirmation message
        label = QLabel("Are you sure you want to quit?")
        label.setFont(QFont("Helvetica", 18))
        label.setStyleSheet("color: white;")

        # Create Yes and No buttons with corresponding callbacks
        yes_button = SecondaryButton(
            "Yes", self.quit_application
        )  # secondary button that quits the application
        no_button = PrimaryButton(
            "No", self.close_dialog
        )  # primary button that closes the confirmation dialog

        # Add all the widgets to the layout
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0, 1, 1)
        layout.addWidget(no_button, 1, 1, 1, 1)

    # Callback function to quit the application
    def quit_application(self):
        QApplication.quit()

    # Callback function to close the dialog
    def close_dialog(self):
        self.close()
