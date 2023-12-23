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
            # if piece.has_all_nieghbours_of_type(type):
            #     GameLogic.place_piece(type, piece)
            #     GameLogic.decrement_neighbour_liberties(piece)
            #     piece.add_to_group()
            #     GameLogic.check_captures_near(piece)
            #     return True
            # else:  # it is suicide
            #     GameLogic.display_wrong_move()
            #     return False
            GameLogic.place_piece(type, piece)  # place the piece as a test
            GameLogic.decrement_neighbour_liberties(
                piece
            )  # change the liberties of neighbours
            if piece.has_all_nieghbours_of_type(
                type
            ):  # if the pieces on all four sides are the same colour as this piece it is a valid move
                return True
            elif GameLogic.check_captures_near(
                piece
            ):  # if not all four are the same colour then check
                piece.add_to_group()
                return True
            else:
                piece.remove()
                GameLogic.increment_neighbour_liberties()
                GameLogic.display_wrong_move()
                return False
        else:
            if GameLogic.check_for_KO():
                GameLogic.display_wrong_move()
                return False
            else:
                GameLogic.place_piece(type, piece)
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

        pass

    def display_wrong_move():
        print("Thats was a wrong move ")

    def check_for_KO():
        print("proint checking for KO")
        return False

    def place_piece(type, piece):
        piece.type = type

    # def remove_piece(piece):
    #     piece.type = 0
    #     piece.group = None

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
        capture_count = 0
        for group in groups:
            if not (group.check_for_life()):
                print("group found dead")
                removed_pieces = group.remove()
                capture_count += len(removed_pieces)
            else:
                print("group", str(group), "is alive")

        return capture_count

    def print_board():
        for row in GameLogic.board:
            for element in row:
                print(element.type, end=" ")  # Print each element in the row
            print()  # Move to the next line for the next row
        print("****LIBERTIES*******")
        for row in GameLogic.board:
            for element in row:
                print(element.liberties, end=" ")  # Print each element in the row
            print()  # Move to the next line for the next row
        print("*****GROUPS*****")
        print(str(GameLogic.all_groups))

    def get_board_state():
        state = []
        for row in GameLogic.board:
            state_row = []
            for piece in row:
                state_row.append(piece.type)
            state.append(state_row)
        return state

    def make_board_from_state(new_state):
        pass

    # for groups, check how to know whcih group a piece is in. Then for every cpature you will have a function that


logic = GameLogic()

black = True
while True:
    # Get row and column input
    row_input = int(input("Enter y value the row()"))
    column_input = int(input("Enter x value which is the column "))

    if GameLogic.try_move(1 if black else 2, row_input, column_input):
        black = not black
    GameLogic.print_board()
