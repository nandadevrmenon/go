from PyQt6.QtWidgets import QPushButton


class IconButton(QPushButton):
    def __init__(self, icon, on_click_handler, tool_tip):
        super().__init__()
        self.setIcon(icon)
        self.setFixedSize(40, 30)

        self.setStyleSheet(
            """
            QPushButton {
            background-color: #FFD311;
            border: none;
            border-radius : 7px;
            }

            QPushButton:hover {
                background-color: #E9C111; /* Use a slightly darker shade when hovered */
            }

            QPushButton:pressed {
                background-color: #D8B30E; /* Use an even darker shade when pressed */
            }
            """
        )

        self.setToolTip(tool_tip)
        self.clicked.connect(on_click_handler)
