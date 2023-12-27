from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setStyleSheet("background-color: #070114;")

        self.setFixedHeight(200)
        self.setFixedWidth(300)

        layout = QVBoxLayout(self)

        # main title
        title_label = QLabel("Designed and Programmed by:")
        title_label.setFont(QFont("Helvetica", 16))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white;")
        title_label.setWordWrap(True)

        nandadev = QLabel("Nandadev Rajeev Menon")
        nandadev.setFont(QFont("Helvetica", 14))
        nandadev.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nandadev.setStyleSheet("color: white;")
        nandadev.setWordWrap(True)
        nandadev.setFixedHeight(18)

        vallerie = QLabel("Vallerie Pin Zi See")
        vallerie.setFont(QFont("Helvetica", 14))
        vallerie.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vallerie.setStyleSheet("color: white;")
        vallerie.setWordWrap(True)
        vallerie.setFixedHeight(18)

        florryn = QLabel("Pui Kwan Chiew")
        florryn.setFont(QFont("Helvetica", 14))
        florryn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        florryn.setStyleSheet("color: white;")
        florryn.setWordWrap(True)
        florryn.setFixedHeight(18)

        # subtext that is version number
        version_label = QLabel("Version 1.0.0")
        version_label.setFont(QFont("Helvetica", 12))
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: white;")

        # not really sure what other info to add here

        layout.addWidget(title_label)
        layout.addWidget(nandadev)
        layout.addWidget(vallerie)
        layout.addWidget(florryn)
        layout.addWidget(version_label)
