from piece_logic import Piece


class GameLogic:
    player1 = None
    player2 = None
    current_player = None
    board_states = []
    board = []
    all_groups = []
    score_states = []
    turn = 0
    temp_captured = 0

    def __init__(self, player1, player2):
        GameLogic.player1 = player1
        GameLogic.player2 = player2
        GameLogic.current_player = player1
        GameLogic.temp_captured = 0

        GameLogic.board_states = [None]
        GameLogic.board = []
        GameLogic.all_groups = []
        GameLogic.score_states = [None, {"p1": [0, 0], "p2": [0, 0]}]

        for i in range(7):
            GameLogic.board.append([])
            for j in range(7):
                GameLogic.board[i].append(
                    Piece(i, j, GameLogic.board, GameLogic.all_groups)
                )

        GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))
        turn = len(GameLogic.board_states)

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
                        GameLogic.temp_captured = 0
                        return False
                    GameLogic.board = sample_board
                    GameLogic.all_groups = sample_board_groups
                    GameLogic.update_board_scores_turn()
                    return True
                piece.increment_neighbour_liberties()
                piece.remove()
                return False
            else:
                GameLogic.check_captures_near(added_piece)
                GameLogic.board = sample_board
                GameLogic.all_groups = sample_board_groups
                GameLogic.update_board_scores_turn()
                return True
        else:
            piece.place(type)
            piece.decrement_neighbour_liberties()
            piece.add_to_group()
            GameLogic.check_captures_near(piece)
            GameLogic.update_board_scores_turn()
            return True

    def update_board_scores_turn():
        GameLogic.update_player_scores()
        GameLogic.record_board_state()
        GameLogic.current_player = (
            GameLogic.player1
            if GameLogic.current_player is GameLogic.player2
            else GameLogic.player2
        )

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
            if group.stones[0].type != piece.type and not (group.check_for_life()):
                print("group", str(group), " found dead")
                removed = group.remove()
                print("remoeved", removed)
                GameLogic.temp_captured += removed
                captured = True

        return captured

    @staticmethod
    def get_score_state():
        pass

    @staticmethod
    def update_player_scores():
        GameLogic.current_player["score"][
            0
        ] += 1  # piece has been placed so territory increased by 1
        GameLogic.current_player["score"][1] += GameLogic.temp_captured

        print(GameLogic.current_player is GameLogic.player1)
        other_player = (
            GameLogic.player2
            if GameLogic.current_player is GameLogic.player1
            else GameLogic.player1
        )

        other_player["score"][0] -= GameLogic.temp_captured
        GameLogic.temp_captured = 0

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
        if GameLogic.turn < len(GameLogic.board_states):
            GameLogic.board_states = GameLogic.board_states[: GameLogic.turn]
            GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))
            GameLogic.turn = len(GameLogic.board_states)

            GameLogic.score_states = GameLogic.score_states[: GameLogic.turn]
            GameLogic.score_states.append(GameLogic.get_score_state())
        else:
            GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))
            GameLogic.score_states.append(GameLogic.get_score_state())
            GameLogic.turn += 1

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
    def undo_board():
        print("turn number", GameLogic.turn)
        if GameLogic.turn > 2:
            GameLogic.turn -= 1
            prev_board, prev_groups = GameLogic.make_board_from_state(
                GameLogic.board_states[GameLogic.turn - 1]
            )
            GameLogic.board = prev_board
            GameLogic.all_groups = prev_groups

    def redo_board():
        print("turn number", GameLogic.turn)
        if GameLogic.turn < len(GameLogic.board_states):
            GameLogic.turn += 1
            next_board, next_groups = GameLogic.make_board_from_state(
                GameLogic.board_states[GameLogic.turn - 1]
            )
            GameLogic.board = next_board
            GameLogic.all_groups = next_groups

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
        print(str(GameLogic.player1["score"]), str(GameLogic.player2["score"]))

    # main static variable and static class instantiation


if __name__ == "__main__":
    player1 = {"name": "Joojas", "score": [2, 0], "timer": "asd"}
    player2 = {"name": "asd", "score": [4, 0], "timer": "asd"}
    current_player = player1
    logic = GameLogic(player1, player2)
    # board, groups = GameLogic.make_board_from_state(
    #     [
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 2, 2],
    #         [0, 0, 0, 0, 2, 0, 1],
    #         [0, 0, 0, 0, 0, 2, 1],
    #     ]
    # )

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
        undo_input = str(input("Undo Redo ?"))
        if undo_input == "u":
            GameLogic.undo_board()
        elif undo_input == "r":
            GameLogic.redo_board()
        elif GameLogic.try_move(1 if black else 2, row_input, column_input):
            black = not black
        GameLogic.print_board(GameLogic.board)
