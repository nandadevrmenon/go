from piece import Piece


class GameLogic:
    board = []

    for i in range(8):
        board.append([])
        for j in range(8):
            board[i].append(Piece(i, j, board))

    def place_piece(color, y, x):
        # check is theres a piece there
        # check suicide
        # no piece
        # check liberties
        # check KO

        # add it to group

        pass

    # for groups, check how to know whcih group a piece is in. Then for every cpature you will have a function that


logic = GameLogic()

print(logic.board[6][0].calculate_liberties())
