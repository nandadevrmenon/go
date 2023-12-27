import sys
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QWidget,
    QStackedWidget,
    QSizePolicy,
    QScrollArea,
    QApplication,
)
from PyQt6.QtGui import QIcon, QFont, QFontDatabase, QPixmap
from SecondaryButton import SecondaryButton
from PrimaryButton import PrimaryButton
from PyQt6.QtCore import Qt
from PyQt6 import QtCore


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # main widget setup
        self.setWindowTitle("Help")
        self.setStyleSheet("background-color: #070114;")
        self.setFixedHeight(500)
        self.setFixedWidth(420)
        self.setModal(False)

        self.stacked_widget = QStackedWidget()  # stacked widget with mutliple pages

        # the text for the pages in the StackedWidget
        self.pages = [
            {
                "title": "Welcome",
                "image_path": "/images/go.png",
                "content": (
                    "Welcome to Go Game, "
                    "a strategic board game originating from ancient China. "
                    "It's known for its simple rules yet immense strategic depth, making it one"
                    " of the most complex and captivating strategy games."
                ),
            },
            {
                "title": "How to Play",
                "image_path": "/images/how_to_play.png",
                "content": (
                    "The players take turns placing black and white pieces called stones on the grid. "
                    "Black usually takes the first move and play one stone per turn."
                    "The stones are placed where the lines intersect. These intersections are called points."
                ),
            },
            {
                "title": "Liberties",
                "image_path": "/images/liberties.png",
                "content": (
                    "Once a stone is placed on the board, it cannot be moved unless it is captured."
                    "Stones are captured when they have no liberties remaining."
                    "Liberties refer to the open adjacent intersections surrounding a stone."
                    "For instance, a stone positioned at the center of the board has four liberties, "
                    "while a stone on the board's edge possesses three liberties. Stones placed in the corners "
                    "of the board have only two liberties."
                ),
            },
            {
                "title": "Atari",
                "image_path": "/images/atari.png",
                "content": (
                    "When a stone is left with only one liberty, it's termed 'in atari'. "
                    "If the opposing player doesn't respond, those stones risk being captured on the next move"
                ),
            },
            {
                "title": "Captured",
                "image_path": "/images/captured.png",
                "content": (
                    "Stones devoid of liberties are captured and taken off the board. "
                    "These captured stones are set aside for scoring at the game's conclusion."
                ),
            },
            {
                "title": "Group",
                "image_path": "/images/groups.png",
                "content": (
                    "Connected stones of the same color form a group. Such groups share liberties. "
                    "group 'A' has 6 liberties. To capture Black, White needs to occupy all 6 liberties, "
                    "especially since group 'B' is in atari."
                ),
            },
            {
                "title": "Suicide Rule",
                "image_path": "/images/suicide.png",
                "content": (
                    "In A , White cannot play at the point marked with a circle. White would have no liberties "
                    "and be immediately recaptured. This is called suicide, and is forbidden in most rulesets. "
                    "However, in B (bottom-left), the two Black stones also only have one liberty left. In this case, "
                    "White can play at the point marked with a circle. This would capture the Black stones. C shows the result."
                ),
            },
            {
                "title": "Ko Rule",
                "image_path": "/images/ko.png",
                "content": (
                    "Ko is a situation in which Black and White could continue recapturing each other. "
                    "In A, White can capture Black by playing at the square. B is the result. "
                    "However, Black could also play at the square, and resulted A "
                    "The rule of ko: A stone captured in ko cannot be recaptured immediately. "
                    "You must wait at least one turn before recapturing a stone in the ko position."
                ),
            },
            {
                "title": "Scoring System",
                "image_path": "/images/go.png",
                "content": (
                    "The final score are calculated such as \n"
                    "the number of stones placed on the board + captured opponent pieces + territories + kumi(if any)"
                ),
            },
        ]

        self.current_page = 0  # start with first page

        for page_data in self.pages:
            page = self.create_page(
                page_data["title"], page_data["image_path"], page_data["content"]
            )  # for each element we create a page
            self.stacked_widget.addWidget(page)  # and add it to the main stacked widget

        layout = QVBoxLayout(self)  # layout for the dialog

        prev_button = SecondaryButton(
            "Previous", self.show_prev_page
        )  # to show previous page
        next_button = PrimaryButton("Next", self.show_next_page)  # to show next page

        layout.addWidget(self.stacked_widget)
        layout.addWidget(next_button)
        layout.addWidget(prev_button)

        self.setWindowIcon(QIcon("icons/sad.png"))

    def create_page(self, title, image_path, content):
        # Function to create a page with given title and content
        page = QWidget()

        title_label = QLabel(title)  # title that is white with wordwrap and is centered
        title_label.setFont(QFont(self.get_statliches_font(), 35))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white;")
        title_label.setWordWrap(True)
        title_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        image_label = QLabel(self)  # image with 10 px pading and centered
        pixmap = QPixmap(QtCore.QDir.currentPath() + image_path)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("QLabel { padding: 10px; }")

        content_label = QLabel(content)  # readable text that is white and word wrapped
        content_label.setFont(QFont("Helvetica", 16))
        content_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_label.setStyleSheet("color: white;")
        content_label.setWordWrap(True)

        scroll_area = QScrollArea(page)  # Make the content inside the scrollable
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.addWidget(content_label)
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.addWidget(title_label)  # add title and text to page
        layout.addWidget(image_label)
        # layout.addWidget(content_label)
        layout.addWidget(scroll_area)
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
