from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class Board(QFrame):  # base the board on a QFrame widget
    # signal sent when the timer is updated
    updateTimerSignal = pyqtSignal(int)
    clickLocationSignal = pyqtSignal(
        str
    )  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 8  # board is 7 squares wide # TODO - DONE this needs updating
    boardHeight = 8  #
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from


    def __init__(self, player1, player2, currentPlayer):
        super().__init__()
        self.initBoard()
        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = currentPlayer

    def initBoard(self):
        """initiates board"""
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(
            self.timerEvent
        )  # connect timeout signal to timerEvent method
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
        """prints the boardArray in an attractive way"""
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
        return self.boardWidth * 8
        # return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        """returns the height of one square of the board"""
        return self.boardHeight * 8
        # return self.contentsRect().height() / self.boardHeight

    def start(self):
        """starts game"""
        self.isStarted = (
            True  # set the boolean which determines if the game has started to TRUE
        )
        self.resetGame()  # reset the game
        # start the timer with the correct speed
        self.timer.start(self.timerSpeed)
        print("start () - timer is started")

    def timerEvent(self):
        """this event is automatically called when the timer is updated. based on the timerSpeed variable"""
        # TODO - DONE adapt this code to handle your timers
        if self.counter == 0:
            print("Game over")
            self.timer.stop()
            return None
        self.counter -= 1
        print("timerEvent()", self.counter)
        self.updateTimerSignal.emit(self.counter)

    def paintEvent(self, event):
        """paints the board and the pieces of the game"""
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        """this event is automatically called when the mouse is pressed"""
        painter = QPainter(self)
        clickPos = event.pos()
        
        row = clickPos.x() // (self.height() // 7)
        col = clickPos.y() // (self.width() // 8)
        print("height = ", self.height(), self.width())
        print(row, col)

        valid_move = self.tryMove(col + 1, row + 1)
        if valid_move:
            self.drawPieces(painter)
        elif not valid_move:
            self.drawPieces(painter)

        self.update()

    def resetGame(self):
        """clears pieces from the board"""
        # TODO write code to reset game
        self.boardArray = []

    def tryMove(self, newX, newY):
        self.boardArray[newX][newY] = 1
        print(self.boardArray)
        return True

    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        squareWidth = int(self.squareWidth())
        squareHeight = int(self.squareHeight())
        statliches = self.get_statliches_font()
        darkBrown = QColor(101, 67, 33)  # Dark brown color
        woodBrown = QColor(193, 154, 107)  # Wood brown color
        borderThickness = 5  # border size

        row_labels = ["", "1", "2", "3", "4", "5", "6", "7", ""]
        col_labels = ["", "A", "B", "C", "D", "E", "F", "H", ""]
        font = QFont(statliches, 24)  # Font for the labels

        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                painter.translate(col * squareWidth, row * squareHeight)

                # Draw background for all squares
                painter.fillRect(0, 0, squareWidth, squareHeight, woodBrown)

                # Exclude borders for label squares
                if row > 0 and col > 0 and row < 7 and col < 7:
                    painter.fillRect(0, 0, squareWidth, borderThickness, darkBrown)  # Top border
                    painter.fillRect(0, 0, borderThickness, squareHeight, darkBrown)  # Left border
                    painter.fillRect(squareWidth - borderThickness, 0, borderThickness, squareHeight, darkBrown)  # Right border
                    painter.fillRect(0, squareHeight - borderThickness, squareWidth, borderThickness, darkBrown)  # Bottom border

                # Add labels without border
                if row == 0:
                    text = col_labels[col]
                    painter.setFont(font)
                    painter.setPen(QColor(50, 70, 90))

                    painter.drawText(borderThickness - (font.pointSize()//2), squareHeight//10 + font.pointSize(), text)
                    
                if col == 0:
                    text = row_labels[row]
                    painter.setFont(font)
                    painter.setPen(QColor(50, 70, 90))
                    painter.drawText(
                        borderThickness + (font.pointSize() // 2),
                        int(squareHeight - font.pointSize() * 2.5),
                        text,
                    )

                painter.restore()

    def drawPieces(self, painter):
        """draw the pieces on the board"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        black_stone = QPixmap(QtCore.QDir.currentPath() + "/images/black_piece.png")
        white_stone = QPixmap(QtCore.QDir.currentPath() + "/images/white_piece.png")

        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(col * self.squareWidth(), row * self.squareHeight())

                # TODO - DONE draw some pieces as ellipses,  and set the painter brush to the correct color
                if self.boardArray[row][col] == 1:  # Black stone
                    pieceColor = QColor(0, 0, 0)  # Set brush color to black
                    # stone_image = black_stone
                elif self.boardArray[row][col] == 2:  # White stone
                    # Set brush color to white
                    pieceColor = QColor(255, 255, 255)
                    # stone_image = white_stone
                else:
                    painter.restore()
                    continue  # Empty intersection, move to the next

                radius = int((self.squareWidth() - 2) / 2.2)
                center = QPoint(0, 0)

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
