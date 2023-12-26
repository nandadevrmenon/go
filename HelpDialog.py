from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QWidget,
    QStackedWidget,
    QSizePolicy,
)
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from SecondaryButton import SecondaryButton
from PrimaryButton import PrimaryButton
from PyQt6.QtCore import Qt
from PyQt6 import QtCore


class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        # main widget setup
        self.setWindowTitle("Help")
        self.setStyleSheet("background-color: #070114;")
        self.setFixedHeight(400)
        self.setFixedWidth(420)

        self.stacked_widget = QStackedWidget()  # stacked widget with mutliple pages

        # the text for the pages in the StackedWidget
        self.pages = [
            {
                "title": "Welcome",
                "content": (
                    "Welcome to Pictionary, a fun 2-player drawing and guessing game! "
                    "One player draws, and the other guesses. Earn points for guessing "
                    "correctly or showcasing your drawing skills."
                ),
            },
            {
                "title": "How to Play",
                "content": (
                    "- Take turns drawing and guessing.\n"
                    "- Points: 1 for guessing, 2 for drawing.\n"
                    "- A 1-minute timer adds excitement.\n"
                    "- You can skip turns if needed."
                ),
            },
            {
                "title": "Game Interaction",
                "content": (
                    "The timer starts when the drawer first sees the word. The drawer then has 1 minute to make the guesser guess the word."
                    "The drawer can use multiple colours to draw on the canvas to show the guesser what the words is."
                    "You also have the option to skip turns if it gets too challenging."
                ),
            },
            {
                "title": "Tips and Shortcuts",
                "content": (
                    "- Tooltips guide you on buttons.\n"
                    "- Right-click a color to fill the canvas with that color.\n"
                    "- Adjust brush size with Ctrl = or Ctrl -.\n"
                    "- Shortcuts for saving, clearing, and more."
                ),
            },
            {
                "title": "Shortcuts ",
                "content": "- Ctrl + = to increase brush size\n- Ctrl + - to decrease brush size\n- Ctrl + 1 through Ctrl + 8 to cycle through colors\n- Return key to check answer\n- Ctrl + W to show/hide word\n- Ctrl + P for pen\n- Ctrl + E for eraser\n- Ctrl + U for uploading an image\n- Ctrl + Shift + H for help\n- Ctrl + / for about",
            },
        ]

        self.current_page = 0  # start with first page

        for page_data in self.pages:
            page = self.create_page(
                page_data["title"], page_data["content"]
            )  # for each element we create a page
            self.stacked_widget.addWidget(page)  # and add it to the main stacked widget

        layout = QVBoxLayout(self)  # layout for the dialog

        prev_button = SecondaryButton(
            "Previous", self.show_prev_page
        )  # to show previous page
        next_button = PrimaryButton("Next", self.show_next_page)  # to show next page

        layout.addWidget(self.stacked_widget)
        layout.addWidget(prev_button)
        layout.addWidget(next_button)

        self.setWindowIcon(QIcon("icons/sad.png"))

    def create_page(self, title, content):
        # Function to create a page with given title and content
        page = QWidget()

        title_label = QLabel(title)  # title that is white with wordwrap and is centered
        title_label.setFont(QFont(self.get_statliches_font(), 35))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white;")
        title_label.setWordWrap(True)
        title_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        content_label = QLabel(content)  # readable text that is white and word wrapped
        content_label.setFont(QFont("Helvetica", 16))
        content_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_label.setStyleSheet("color: white;")
        content_label.setWordWrap(True)

        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.addWidget(title_label)  # add title and text to page
        layout.addWidget(content_label)
        return page

    def show_next_page(self):
        # Function to show the next page
        current_index = self.stacked_widget.currentIndex()
        next_index = (
            current_index + 1
        ) % self.stacked_widget.count()  # gives us element number is the array insetad of going out of bounds
        self.stacked_widget.setCurrentIndex(next_index)

    def show_prev_page(self):
        # Function to show the previous page
        current_index = self.stacked_widget.currentIndex()
        prev_index = (current_index - 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(prev_index)

    def get_statliches_font(self):
        font_path = QtCore.QDir.currentPath() + "/fonts/statliches.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)  # load font
        # Check if the font was loaded successfully
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            return "Helvetica"  # fallback
