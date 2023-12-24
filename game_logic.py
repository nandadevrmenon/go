from piece_logic import Piece


class GameLogic:
    @staticmethod
    def try_move(type, y, x):
        board = GameLogic.board
        piece = board[y][x]
        if piece.type != 0:  # already a piece there
            return None
        if piece.liberties == 0:  # if piece is surrounded
            piece.place(type)
            piece.decrement_neighbour_liberties()

            state = GameLogic.get_board_state(GameLogic.board)
            sample_board, sample_board_groups = GameLogic.make_board_from_state(state)
            added_piece = sample_board[y][x]

            if GameLogic.check_suicide_for(added_piece):
                print("suicide found ")
                if GameLogic.check_captures_near(added_piece):
                    if GameLogic.check_for_KO(sample_board):
                        piece.increment_neighbour_liberties()
                        piece.remove()
                        return False
                    GameLogic.board = sample_board
                    GameLogic.all_groups = sample_board_groups
                    GameLogic.record_board_state()
                    return True
                piece.increment_neighbour_liberties()
                piece.remove()
                return False
            else:
                GameLogic.check_captures_near(added_piece)
                GameLogic.board = sample_board
                GameLogic.all_groups = sample_board_groups
                GameLogic.record_board_state()
                return True
        else:
            piece.place(type)
            piece.decrement_neighbour_liberties()
            piece.add_to_group()
            GameLogic.check_captures_near(piece)
            GameLogic.record_board_state()
            return True

    @staticmethod
    def check_for_KO(sample_board):
        sample_board_state = GameLogic.get_board_state(sample_board)
        if (
            sample_board_state
            == GameLogic.board_states[len(GameLogic.board_states) - 2]
        ):
            print("KO found")
            return True
        return False

    @staticmethod
    def check_captures_near(piece):
        neighbours = piece.get_neighbours()
        groups = [piece.group for piece in neighbours if piece.group is not None]
        captured = False
        for group in groups:
            if not (group.check_for_life()):
                print("group", str(group), " found dead")
                group.remove()
                captured = True

        return captured

    @staticmethod
    def check_suicide_for(piece):
        neighbours = piece.get_neighbours()
        groups = [piece.group for piece in neighbours if piece.group is not None]
        for group in groups:
            if group == piece.group and not group.check_for_life():
                return True
        if not piece.group.check_for_life():
            return True
        return False

    @staticmethod
    def get_board_state(board):
        state = []
        for row in board:
            state_row = []
            for piece in row:
                state_row.append(piece.type)
            state.append(state_row)
        return state

    @staticmethod
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
                    piece.decrement_neighbour_liberties()
                    piece.add_to_group()

        return (new_board, new_groups)

    @staticmethod
    def record_board_state():
        GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))

    @staticmethod
    def reset_board():
        board_states = [None]
        board = []
        all_groups = []

        for i in range(7):
            board.append([])
            for j in range(7):
                board[i].append(Piece(i, j, board, all_groups))

        board_states.append(GameLogic.get_board_state(board))

    @staticmethod
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

    # main static variable and static class instantiation

    board_states = [None]
    board = []
    all_groups = []

    for i in range(7):
        board.append([])
        for j in range(7):
            board[i].append(Piece(i, j, board, all_groups))

    board_states.append(get_board_state(board))


if __name__ == "__main__":
    logic = GameLogic()
    board, groups = GameLogic.make_board_from_state(
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 2, 0, 1],
            [0, 0, 0, 0, 0, 2, 1],
        ]
    )
    GameLogic.board = board
    GameLogic.all_groups = groups
    GameLogic.record_board_state()
    black = True
    while True:
        # Get row and column input
        row_input = int(input("Enter y value the row()"))
        column_input = int(input("Enter x value which is the column "))

        if GameLogic.try_move(1 if black else 2, row_input, column_input):
            black = not black
        GameLogic.print_board(GameLogic.board)
