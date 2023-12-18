from PyQt6.QtWidgets import QApplication
from StartScreen import StartScreen
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartScreen()  # open the start screen of the game
    window.show()
    app.exec()  # start the event loop running
