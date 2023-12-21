from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import QPoint


class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(
        str
    )  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 6  # board is 7 squares wide # TODO - DONE this needs updating
    boardHeight = 6  #
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
            # [(0 for i in range(7)) for i in range(7)]
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
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
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
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
        clickLoc = (
            "click location [" + str(event.x()) + "," + str(event.y()) + "]"
        )  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        """clears pieces from the board"""
        # TODO write code to reset game
        self.boardArray = []

    def tryMove(self, newX, newY):
        """tries to move a piece"""
        pass  # Implement this method according to your logic

    def drawBoardSquares(self, painter):
        """draw all the square on the board"""
        squareWidth = int(self.squareWidth())
        squareHeight = int(self.squareHeight())
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                painter.translate(col * squareWidth, row * squareHeight)
                painter.setBrush(QBrush(QColor(0, 0, 0)))  # Set brush color
                painter.drawRect(0, 0, squareWidth, squareHeight)  # Draw rectangles
                painter.restore()

    def drawPieces(self, painter):
        """draw the pieces on the board"""
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(col * self.squareWidth(), row * self.squareHeight())
                # TODO - DONE draw some pieces as ellipses,  and set the painter brush to the correct color
                if self.currentPlayer == self.player1:  # Black stone
                    painter.setBrush(QColor(0, 0, 0))  # Set brush color to black
                else:
                    painter.setBrush(QColor(255, 255, 255))  # Set brush color to white
                radius = int((self.squareWidth()-2 ) / 3)
                center = QPoint(radius, radius)
                painter.drawEllipse(center, radius, radius)
                  

