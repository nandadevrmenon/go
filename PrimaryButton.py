from PyQt6.QtWidgets import QPushButton, QWidget


class PrimaryButton(QPushButton):
    def __init__(self, text, on_click_handler):
        super().__init__(text)

        # Set default styles
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #FFD518; /* Default background color (green) */
                color: #141414; /* Default font color */
                border: 1px solid #FFD518; /* Border color */
                border-radius: 5px; /* Border radius */
                padding: 5px 10px; /* Padding */
            }
            
            QPushButton:hover {
                background-color: #E9C111; /* Hover background color */
            }
            
            QPushButton:pressed {
                background-color:#D8B30E; /* Clicked background color (darker green) */
            }
        """
        )

        self.clicked.connect(
            on_click_handler
        )  # passes the callback into the native clicked event handler
