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
        self.try_move = try_move  # the try move call back that calls try move in the game logic and also updates the UI accordingly

        self.initBoard()  # draw the inital board (which is only used for drawing the board)/ actual logical board in GameLogic
        self.setFixedWidth(640)
        self.setFixedHeight(640)

        # Timer for valid and invalid move Animation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.updateAnimation)
        self.animation_radius = int((self.squareWidth() - 2) / 2.2) + 10
        self.animation_finished = False
        self.animation_timer.start(30)
        self.opacity = 1
        self.animation_radius = int((self.squareWidth() - 2) / 2.2)

        # Timer for captured pieces animation
        self.captured_pieces = []
        self.group_animation_timer = QTimer(self)
        self.group_animation_timer.timeout.connect(self.update_captured_animation)
        self.group_opacity = 1
        self.group_animation_finished = False
        self.group_animation_timer.start(30)

        # temp variables that hold the x y value of the pieces for the animations ,better to have class variables than passing it into every method
        self.x = None
        self.y = None
        self.move_validity = None

    def initBoard(self):
        self.boardArray = (
            [7, 7, 7, 7, 7, 7, 7, 7, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 0, 0, 0, 0, 0, 0, 0, 7],
            [7, 7, 7, 7, 7, 7, 7, 7, 7],
        )  # TODO - DONE create a 2d int/Piece array to store the state of the game
        # self.printBoardArray()  # TODO - DONE uncomment this method after creating the array above

    def squareWidth(self):
        """returns the width of one square in the board"""
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        """returns the height of one square of the board"""
        return self.contentsRect().height() / self.boardHeight

    def paintEvent(self, event):
        """paints the board and the pieces of the game"""
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 0, 0, 0)))
        self.drawBoardSquares(painter)
        self.drawPieces(painter)  # draws all pieces
        self.animatePieces(
            painter
        )  # animates any pieces that were added in the last turn
        self.capturedAnimation(
            painter, self.captured_pieces
        )  # animateds any pieces that were captureed in the last turn

    def mousePressEvent(self, event):
        """this event is automatically called when the mouse is pressed"""
        clickPos = event.pos()

        # convert the mouse click coordinate to row & col index on the board
        row = clickPos.x() // (self.height() // 7)
        col = clickPos.y() // (self.width() // 7)
        self.move_validity, self.captured_pieces = self.try_move(col, row)

        self.x = row
        self.y = col

        # reset timer for pieces animation
        if self.animation_timer.isActive():
            self.animation_timer.stop()

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.updateAnimation)

        if self.move_validity:  # valid move animation
            self.animation_radius = int((self.squareWidth() - 2) / 2.2) + 10
            if self.captured_pieces != [] and self.group_opacity < 1:
                self.group_animation_timer = QTimer(self)
                self.group_animation_timer.timeout.connect(
                    self.update_captured_animation
                )
                self.group_opacity = 1
                self.group_animation_finished = False
                self.group_animation_timer.start(30)
        else:  # invalid move animation
            self.animation_radius = int((self.squareWidth() - 2) / 2.2)
            self.opacity = 1
        self.animation_finished = False
        self.animation_timer.start(30)

        self.update()

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
        for row in range(0, len(GameLogic.board)):
            for col in range(0, len(GameLogic.board[0])):
                painter.save()
                painter.translate(
                    (col + 1) * self.squareWidth(), (row + 1) * self.squareHeight()
                )

                # TODO - DONE draw some pieces as ellipses,  and set the painter brush to the correct color
                if GameLogic.board[row][col].type == 1:  # Black stone
                    # Set brush color to black
                    pieceColor = QColor(0, 0, 0)
                elif GameLogic.board[row][col].type == 2:  # White stone
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

    def animatePieces(self, painter):
        row = self.y
        col = self.x
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pieceColor = QColor(0, 0, 0, 0)
        if self.move_validity is None or (self.x is None and self.y is None):
            pass
        elif self.move_validity:
            # painter.translate(col * self.squareWidth(), row * self.squareHeight())
            if GameLogic.board[row][col].type == 1:  # Black stone
                pieceColor = QColor(0, 0, 0)  # Set brush color to black
                # stone_image = black_stone
            elif GameLogic.board[row][col].type == 2:  # White stone
                # Set brush color to white
                pieceColor = QColor(255, 255, 255)
            else:
                painter.restore()
            # Draw the piece
            painter.setBrush(pieceColor)
            painter.drawEllipse(
                QPoint(
                    (col + 1) * int(self.squareWidth()),
                    (row + 1) * int(self.squareHeight()),
                ),
                self.animation_radius,
                self.animation_radius,
            )

        else:
            # invalid move - red flash
            color = QColor(255, 0, 0, int(self.opacity * 255))
            painter.setBrush(color)
            painter.drawEllipse(
                QPoint(
                    (col + 1) * int(self.squareWidth()),
                    (row + 1) * int(self.squareHeight()),
                ),
                self.animation_radius,
                self.animation_radius,
            )

    def updateAnimation(self):
        if self.move_validity:
            if not self.animation_finished:
                self.animation_radius -= 1
                self.update()
            if self.animation_radius == int((self.squareWidth() - 2) / 2.2):
                self.animation_finished = True
                self.move_validity = None
                self.animation_timer.stop()
        else:
            if not self.animation_finished:
                self.opacity -= 0.05  # Decrease opacity (change this value as needed)
                self.update()
            if self.opacity <= 0:
                self.animation_finished = True
                self.move_validity = None
                self.animation_timer.stop()
                return
            # Trigger widget repaint

    def capturedAnimation(self, painter, captured_group):
        color = QColor(0, 0, 0, 0)
        if captured_group is None:
            pass
        else:
            for i in captured_group:
                if i[2] == 1:  # check the type of peices and set the brushColor
                    color = QColor(0, 0, 0, int(self.group_opacity * 255))
                else:
                    color = QColor(255, 255, 255, int(self.group_opacity * 255))

                painter.setBrush(color)
                painter.drawEllipse(
                    QPoint(
                        (i[1] + 1) * int(self.squareWidth()),
                        (i[0] + 1) * int(self.squareHeight()),
                    ),
                    self.animation_radius,
                    self.animation_radius,
                )

    def update_captured_animation(self):
        if not self.group_animation_finished:
            self.group_opacity -= 0.05  # Decrease opacity
            if self.group_opacity == 0:
                self.group_animation_finished = True
                self.move_validity = None
                self.group_animation_timer.stop()

    def get_statliches_font(self):
        font_path = QtCore.QDir.currentPath() + "/fonts/statliches.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)  # load font
        # Check if the font was loaded successfully
        if font_id != -1:
            return QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            return "Helvetica"  # fallback
