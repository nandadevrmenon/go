from piece import Piece


class GameLogic:
    turn = 0
    board_states = []
    board = []
    all_groups = []

    for i in range(7):
        board.append([])
        for j in range(7):
            board[i].append(Piece(i, j, board, all_groups))

    def try_move(type, y, x):
        board = GameLogic.board
        piece = board[y][x]
        if piece.type != 0:  # already a piece there
            return None
        if piece.liberties == 0:  # if piece is surrounded
            piece.place(type)
            GameLogic.decrement_neighbour_liberties(piece)

            state = GameLogic.get_board_state(GameLogic.board)
            sample_board, sample_board_groups = GameLogic.make_board_from_state(state)

            added_piece = sample_board[y][x]
            if GameLogic.check_suicide_for(added_piece):
                print("suicide")
                if GameLogic.check_captures_near(added_piece):
                    GameLogic.board = sample_board
                    GameLogic.all_groups = sample_board_groups
                    return True
                GameLogic.increment_neighbour_liberties(piece)
                piece.remove()
                return False
            else:
                GameLogic.check_captures_near(added_piece)
                GameLogic.board = sample_board
                GameLogic.all_groups = sample_board_groups
                return True

        else:
            if GameLogic.check_for_KO():
                GameLogic.display_wrong_move()
                return False
            else:
                piece.place(type)
                GameLogic.decrement_neighbour_liberties(piece)
                piece.add_to_group()
                GameLogic.check_captures_near(piece)
                return True

        # check is theres a piece there
        # check suicide
        # no piece
        # check liberties
        # check KO

        # add it to group

    def display_wrong_move():
        print("Thats was a wrong move ")

    def check_for_KO():
        print("proint checking for KO")
        return False

    # def remove_piece(piece):
    #     piece.type = 0
    #     piece.group = None

    def remove(piece):
        piece.type = 0
        piece.group = None

    def decrement_neighbour_liberties(piece):
        neighbours = piece.get_neighbours()
        for piece in neighbours:
            piece.liberties = piece.liberties - 1

    def increment_neighbour_liberties(piece):
        neighbours = piece.get_neighbours()
        for piece in neighbours:
            piece.liberties = piece.liberties + 1

    def check_captures_near(piece):
        neighbours = piece.get_neighbours()
        groups = [piece.group for piece in neighbours if piece.group is not None]
        captured = False
        for group in groups:
            if not (group.check_for_life()):
                print("group found dead")
                group.remove()
                captured = True

            else:
                print("group", str(group), "is alive")

        return captured

    def check_suicide_for(piece):
        neighbours = piece.get_neighbours()
        groups = [piece.group for piece in neighbours if piece.group is not None]
        for group in groups:
            if group == piece.group and not group.check_for_life():
                return True
        if not piece.group.check_for_life():
            return True
        return False

    def print_board(board):
        for row in board:
            for element in row:
                print(element.type, end=" ")  # Print each element in the row
            print()  # Move to the next line for the next row
        print("****LIBERTIES*******")
        for row in board:
            for element in row:
                print(element.liberties, end=" ")  # Print each element in the row
            print()  # Move to the next line for the next row
        print("*****GROUPS*****")
        print(str(GameLogic.all_groups))

    def get_board_state(board):
        state = []
        for row in board:
            state_row = []
            for piece in row:
                state_row.append(piece.type)
            state.append(state_row)
        return state

    def make_board_from_state(state):
        new_board = []
        new_groups = []
        for i in range(7):
            new_board.append([])
            for j in range(7):
                piece = Piece(i, j, new_board, new_groups)
                piece.type = state[i][j]
                new_board[i].append(piece)

        for row in new_board:
            for piece in row:
                if piece.type != 0:
                    GameLogic.decrement_neighbour_liberties(piece)
                    piece.add_to_group()

        return (new_board, new_groups)

    # for groups, check how to know whcih group a piece is in. Then for every cpature you will have a function that


logic = GameLogic()
board, groups = GameLogic.make_board_from_state(
    [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 2, 1, 2, 0, 0],
        [0, 2, 1, 0, 1, 2, 0],
        [0, 0, 2, 1, 2, 0, 0],
        [0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
)

GameLogic.board = board
GameLogic.all_groups = groups
black = True
while True:
    # Get row and column input
    row_input = int(input("Enter y value the row()"))
    column_input = int(input("Enter x value which is the column "))

    if GameLogic.try_move(1 if black else 2, row_input, column_input):
        black = not black
    GameLogic.print_board(GameLogic.board)
