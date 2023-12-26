from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt


class OverlayExample(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main widget and set a layout
        main_layout = QVBoxLayout(self)

        # Create the background widget (QFrame in this case)
        background_widget = QFrame(self)
        background_widget.setStyleSheet("background-color: lightgray;")
        main_layout.addWidget(background_widget)

        # Create the overlay widget (in this case, a QLabel)
        overlay_widget = QLabel("Overlay Widget", self)
        overlay_widget.setStyleSheet("background-color: rgba(255, 0, 0, 100);")
        overlay_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(overlay_widget)
        overlay_widget.raise_()


if __name__ == "__main__":
    app = QApplication([])
    window = OverlayExample()
    window.setGeometry(100, 100, 400, 300)
    window.show()
    app.exec()
