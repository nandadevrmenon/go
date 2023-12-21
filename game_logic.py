from piece import Piece


class GameLogic:
    board = []

    for i in range(8):
        board.append([])
        for j in range(8):
            board[i].append(Piece(i, j, board))

    def place_piece(color, y, x):
        # check suicide
        # check KO
        # check is theres a piece there
        # no piece
        pass


logic = GameLogic()

print(logic.board[6][0].calculate_liberties())
