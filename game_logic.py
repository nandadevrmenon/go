from piece_logic import Piece
from PyQt6.QtCore import Qt, QTimer


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

    def __init__(self, p1Name=None, p2Name=None):
        if p1Name is not None and p2Name is not None:
            GameLogic.player1 = {"name": p1Name, "score": [12, 2], "timer": QTimer()}
            GameLogic.player2 = {"name": p2Name, "score": [1, 78], "timer": QTimer()}
            GameLogic.current_player = GameLogic.player1
            GameLogic.temp_captured = 0

            GameLogic.board_states = [
                None,
            ]
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
            GameLogic.turn = len(GameLogic.board_states)

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
        GameLogic.flip_turn()

    def flip_turn():
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
            if (
                group.stones
                and group.stones[0].type != piece.type
                and not (group.check_for_life())
            ):
                removed = group.remove()
                GameLogic.temp_captured += removed
                captured = True

        return captured

    @staticmethod
    def get_score_state():
        p1 = GameLogic.player1
        p2 = GameLogic.player2
        return {
            "p1": [p1["score"][0], p1["score"][1]],
            "p2": [p2["score"][0], p2["score"][1]],
        }

    def set_scores_using(state):
        GameLogic.player1["score"][0] = state["p1"][0]
        GameLogic.player1["score"][1] = state["p1"][1]
        GameLogic.player2["score"][0] = state["p2"][0]
        GameLogic.player2["score"][1] = state["p2"][1]

    @staticmethod
    def update_player_scores():
        GameLogic.current_player["score"][
            0
        ] += 1  # piece has been placed so territory increased by 1
        GameLogic.current_player["score"][1] += GameLogic.temp_captured
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

            GameLogic.score_states = GameLogic.score_states[: GameLogic.turn]
            GameLogic.score_states.append(GameLogic.get_score_state())
            GameLogic.turn = len(GameLogic.board_states)
        else:
            GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))
            GameLogic.score_states.append(GameLogic.get_score_state())
            GameLogic.turn += 1

    @staticmethod
    def reset_board():
        GameLogic.board_states = [None]
        GameLogic.board = []
        GameLogic.all_groups = []
        GameLogic.current_player = GameLogic.player1
        for i in range(7):
            GameLogic.board.append([])
            for j in range(7):
                GameLogic.board[i].append(
                    Piece(i, j, GameLogic.board_states, GameLogic.all_groups)
                )

        GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))

    @staticmethod
    def undo_board():
        if GameLogic.turn > 2:
            GameLogic.turn -= 1
            prev_board, prev_groups = GameLogic.make_board_from_state(
                GameLogic.board_states[GameLogic.turn - 1]
            )
            prev_score_state = GameLogic.score_states[GameLogic.turn - 1]
            GameLogic.set_scores_using(prev_score_state)
            GameLogic.board = prev_board
            GameLogic.all_groups = prev_groups
            GameLogic.flip_turn()

    def redo_board():
        if GameLogic.turn < len(GameLogic.board_states):
            next_board, next_groups = GameLogic.make_board_from_state(
                GameLogic.board_states[GameLogic.turn]
            )
            next_score_state = GameLogic.score_states[GameLogic.turn]
            GameLogic.set_scores_using(next_score_state)
            GameLogic.board = next_board
            GameLogic.all_groups = next_groups
            GameLogic.flip_turn()
            GameLogic.turn += 1

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
    logic = GameLogic("hello", "ruh")
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

    # board, groups = GameLogic.make_board_from_state(
    #     [
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #     ]
    # )

    # GameLogic.board = board
    # GameLogic.all_groups = groups
    # GameLogic.record_board_state()
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
        print(len(GameLogic.board_states), len(GameLogic.score_states), GameLogic.turn)
        print(str(GameLogic.score_states))
