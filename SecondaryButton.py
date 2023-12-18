from PyQt6.QtWidgets import QPushButton


class SecondaryButton(QPushButton):
    def __init__(self, text, on_click_handler):
        super().__init__(text)

        # Set default styles
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #9CAFB7; /* Default background color (dull blue) */
                color: #141414; /* Default font color */
                border: 1px solid #9CAFB7; /* Border color */
                border-radius: 5px; /* Border radius */
                padding: 5px 10px; /* Padding */
            }

            QPushButton:hover {
                background-color: #91A5AD; /* Hover background color */
            }

            QPushButton:pressed {
                background-color: #69849A; /* Clicked background color (darker blue) */
            }
            """
        )

        self.clicked.connect(on_click_handler)
