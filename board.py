from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from game_logic import GameLogic


class Board(QFrame):  # base the board on a QFrame widget
    # signal sent when the timer is updated

    # TODO set the board width and height to be square
    boardWidth = 8  # board is 7 squares wide # TODO - DONE this needs updating
    boardHeight = 8  #

    def __init__(self, try_move):
        super().__init__()
        self.try_move = try_move
        self.started = 4
        self.initBoard()
        self.setFixedWidth(640)
        self.setFixedHeight(640)

    def initBoard(self):
        """initiates board"""

        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.boardArray = (
            [7, 7, 7, 7, 7, 7, 7, 7, 7],
            [7, 0, 0, 0, 2, 2, 0, 0, 7],
            [7, 0, 0, 1, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7],
        )  # TODO - DONE create a 2d int/Piece array to store the state of the game
        self.printBoardArray()  # TODO - DONE uncomment this method after creating the array above

    def printBoardArray(self):
        """prints the boardArray to console in an attractive way"""
        print("boardArray:")
        print(
            "\n".join(
                ["\t".join([str(cell) for cell in row]) for row in self.boardArray]
            )
        )

    def mousePosToColRow(self, event):
        """convert the mouse click event to a row and column"""
        pass  # Implement this method according to your logic

    def squareWidth(self):
        """returns the width of one square in the board"""
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        """returns the height of one square of the board"""
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        """starts game"""
        self.isStarted = (
            True  # set the boolean which determines if the game has started to TRUE
        )
        self.resetGame()  # reset the game
        # start the timer with the correct speed

    def resetGame(self):
        """clears pieces from the board"""
        # TODO write code to reset game
        self.boardArray = []

    def paintEvent(self, event):
        """paints the board and the pieces of the game"""
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        """this event is automatically called when the mouse is pressed"""
        clickPos = event.pos()

        row = clickPos.x() // (self.height() // 7)
        col = clickPos.y() // (self.width() // 8)
        print("height = ", self.height(), self.width())
        print(row, col)

        valid_move = self.try_move(col, row)
        if valid_move:
            self.boardArray[5][5] = 2
            self.update()

        # self.update()

    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        # get the size of the square
        squareWidth = int(self.squareWidth())
        squareHeight = int(self.squareHeight())

        # get the font for the application
        statliches = self.get_statliches_font()
        font = QFont(statliches, 24)  # Font for the labels

        darkBrown = QColor(101, 67, 33)  # Dark brown color
        woodBrown = QColor(193, 154, 107)  # Wood brown color
        borderThickness = 5  # border size

        # labels to print out on the board
        row_labels = ["", "1", "2", "3", "4", "5", "6", "7", ""]
        col_labels = ["", "A", "B", "C", "D", "E", "F", "H", ""]
        # painter.begin(self)
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                painter.translate(col * squareWidth, row * squareHeight)

                # Draw background for all squares
                painter.fillRect(0, 0, squareWidth, squareHeight, woodBrown)

                # Exclude borders for label squares
                if row > 0 and col > 0 and row < 7 and col < 7:
                    painter.fillRect(
                        0, 0, squareWidth, borderThickness, darkBrown
                    )  # Top border
                    painter.fillRect(
                        0, 0, borderThickness, squareHeight, darkBrown
                    )  # Left border
                    painter.fillRect(
                        squareWidth - borderThickness,
                        0,
                        borderThickness,
                        squareHeight,
                        darkBrown,
                    )  # Right border
                    painter.fillRect(
                        0,
                        squareHeight - borderThickness,
                        squareWidth,
                        borderThickness,
                        darkBrown,
                    )  # Bottom border

                # handles the printing of the horizontal label of the board
                if row == 0:
                    text = col_labels[col]
                    painter.setFont(font)
                    painter.setPen(QColor(50, 70, 90))

                    painter.drawText(
                        borderThickness - (font.pointSize() // 2),
                        squareHeight // 10 + font.pointSize(),
                        text,
                    )

                # handles the printing of the vertical label of the board
                if col == 0:
                    text = row_labels[row]
                    painter.setFont(font)
                    painter.setPen(QColor(50, 70, 90))
                    painter.drawText(
                        borderThickness + (font.pointSize() // 2),
                        int(squareHeight - font.pointSize() * 2.9),
                        text,
                    )

                painter.restore()

    def drawPieces(self, painter):
        """draw the pieces on the board"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(col * self.squareWidth(), row * self.squareHeight())

                # TODO - DONE draw some pieces as ellipses,  and set the painter brush to the correct color
                if self.boardArray[row][col] == 1:  # Black stone
                    # Set brush color to black
                    pieceColor = QColor(0, 0, 0)
                elif self.boardArray[row][col] == 2:  # White stone
                    # Set brush color to white
                    pieceColor = QColor(255, 255, 255)
                else:
                    painter.restore()
                    continue  # Empty intersection, move to the next

                # size of the stone piece
                radius = int((self.squareWidth() - 2) / 2.2)
                center = QPoint(0, 0)  # position of the stone piece

                # Draw the piece
                painter.setBrush(pieceColor)
                painter.drawEllipse(center, radius, radius)
                painter.restore()

    def get_statliches_font(self):
        font_path = QtCore.QDir.currentPath() + "/fonts/statliches.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)  # load font
        # Check if the font was loaded successfully
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            return "Helvetica"  # fallback
