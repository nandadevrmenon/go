from piece_logic import Piece
from PyQt6.QtCore import Qt, QTimer


class GameLogic:
    # initialize static class variables
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
        if (
            p1Name is not None and p2Name is not None
        ):  # if the names provided are not none
            # create player dictionaries
            GameLogic.player1 = {"name": p1Name, "score": [0, 0], "timer": QTimer()}
            GameLogic.player2 = {"name": p2Name, "score": [0, 0], "timer": QTimer()}

            # set current player
            GameLogic.current_player = GameLogic.player1

            # temp variable for score management
            GameLogic.temp_captured = 0

            # records all previous board states for undo redo functionality
            GameLogic.board_states = [
                None,
            ]
            GameLogic.board = []  # actual board of pieces
            GameLogic.all_groups = []  # the groups present on the board
            GameLogic.score_states = [
                None,
                {"p1": [0, 0], "p2": [0, 0]},
            ]  # similar to baord states but for player scores

            # fill the board with pieces
            for i in range(7):
                GameLogic.board.append([])
                for j in range(7):
                    GameLogic.board[i].append(
                        Piece(i, j, GameLogic.board, GameLogic.all_groups)
                    )
            GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))
            GameLogic.turn = len(GameLogic.board_states)

    @staticmethod
    def try_move(
        type, y, x
    ):  # -> returns True/False/None for valid_move/suicide or KO/ inavlid move and also the captured pieces
        board = GameLogic.board
        piece = board[y][x]
        if piece.type != 0:  # already a piece there
            return None, None
        if piece.liberties == 0:  # if piece is surrounded
            piece.place(type)  # try the move
            piece.decrement_neighbour_liberties()

            # make a sample board so we can see what happens
            state = GameLogic.get_board_state(GameLogic.board)
            sample_board, sample_board_groups = GameLogic.make_board_from_state(state)
            added_piece = sample_board[y][x]

            captured_pieces = []
            if GameLogic.check_suicide_for(added_piece):  # check if it is suicide
                if (  # if the suicide is for a capture then it is allowed
                    len(captured_pieces := GameLogic.get_captured_pieces(added_piece))
                    > 0
                ):
                    if GameLogic.check_for_KO(
                        sample_board
                    ):  # if capturing,then also check for KO
                        piece.increment_neighbour_liberties()  # if KO found then take board back to its original state
                        piece.remove()
                        GameLogic.temp_captured = 0
                        return False, None
                    GameLogic.board = sample_board  # if no KO then allow the move and update the board state
                    GameLogic.all_groups = sample_board_groups
                    GameLogic.update_board_scores_turn()  # update the baord, the scores of each player and also flip the turns
                    return True, captured_pieces
                piece.increment_neighbour_liberties()  # if suicide not for captrue then take board back to original state
                piece.remove()
                return False, None
            else:
                captured_pieces = GameLogic.get_captured_pieces(
                    added_piece
                )  # if no suicide then update the current board and update everything else like player scores etc
                GameLogic.board = sample_board
                GameLogic.all_groups = sample_board_groups
                GameLogic.update_board_scores_turn()
                return True, captured_pieces
        else:  # if spot has liberties left then place the piece update the liberties of its neighbours and update other stuff like score etc
            piece.place(type)
            piece.decrement_neighbour_liberties()
            piece.add_to_group()
            captured_pieces = GameLogic.get_captured_pieces(piece)
            GameLogic.update_board_scores_turn()
            return True, captured_pieces

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
    def check_for_KO(
        sample_board,
    ):  # checks if current board state is same as board state 2 moves ago
        sample_board_state = GameLogic.get_board_state(sample_board)
        if (
            sample_board_state
            == GameLogic.board_states[len(GameLogic.board_states) - 2]
        ):
            print("KO found")
            return True
        return False

    @staticmethod
    def get_captured_pieces(
        piece,
    ):  # removes captured pieces from board and gets an array of the coordinates of those pieces so as to animate them on the board
        neighbours = piece.get_neighbours()
        groups = [piece.group for piece in neighbours if piece.group is not None]
        captured = []
        for group in groups:
            if (
                group.stones
                and group.stones[0].type != piece.type
                and not (group.check_for_life())
            ):
                for piece in group.stones:
                    captured.append((piece.y, piece.x, piece.type))
                removed = group.remove()
                GameLogic.temp_captured += removed
        return captured

    @staticmethod
    def get_score_state():  # get the state of the score so we can store the score state for undo redo functionality
        p1 = GameLogic.player1
        p2 = GameLogic.player2
        return {
            "p1": [p1["score"][0], p1["score"][1]],
            "p2": [p2["score"][0], p2["score"][1]],
        }

    def set_scores_using(state):  # update the scores using the state given
        GameLogic.player1["score"][0] = state["p1"][0]
        GameLogic.player1["score"][1] = state["p1"][1]
        GameLogic.player2["score"][0] = state["p2"][0]
        GameLogic.player2["score"][1] = state["p2"][1]

    @staticmethod
    def update_player_scores():  # after every turn we udate the scores based on territory and based on pieces captured
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
    def calculate_territories():  # helps in calculating the territories based on stone scoring system suggested by the lecturer at https://senseis.xmp.net/?StoneScoring
        row = len(GameLogic.board)
        col = len(GameLogic.board[0])
        black_territories = 0
        white_territories = 0

        def confirm_territory(y, x):  # see what teriitory an empty space belongs to
            neighbours = GameLogic.board[y][x].get_neighbours()
            color = neighbours[0].type
            for piece in neighbours:
                if piece.type != color:
                    return None
            return color

        for i in range(row):  # for each piece
            for j in range(col):
                if (
                    GameLogic.board[i][j].type == 0
                ):  # if the current position is an empty spot
                    result = confirm_territory(
                        i, j
                    )  # check whose territory and add to thier score
                    if result == 1:
                        black_territories += 1
                    if result == 2:
                        white_territories += 1
        return black_territories, white_territories

    @staticmethod
    def check_suicide_for(piece):  # check suicide checks if the group is alive
        neighbours = piece.get_neighbours()
        groups = [piece.group for piece in neighbours if piece.group is not None]
        for group in groups:
            if (
                group == piece.group and not group.check_for_life()
            ):  # if the move ends in the own pieces group dying off rhen its a suicide move
                return True
        if (
            not piece.group.check_for_life()
        ):  # if its single piece that is not connected to neighbouring groups then
            return True
        return False  # if none of the groups are dying then it is not suicide

    @staticmethod
    def get_board_state(
        board,
    ):  # get the board state as a 2d array of types of the pieces
        state = []
        for row in board:
            state_row = []
            for piece in row:
                state_row.append(piece.type)
            state.append(state_row)
        return state

    @staticmethod
    def make_board_from_state(
        state,
    ):  # takes a board state a makes a baord array of piece objects that as correct liberty values
        new_board = []
        new_groups = []
        for i in range(7):
            new_board.append([])
            for j in range(7):
                piece = Piece(i, j, new_board, new_groups)
                piece.type = state[i][j]
                new_board[i].append(piece)  # eadd pieces

        for row in new_board:  # update the liberties because of those pieces
            for piece in row:
                if piece.type != 0:
                    piece.decrement_neighbour_liberties()
                    piece.add_to_group()

        return (new_board, new_groups)

    @staticmethod
    def record_board_state():  # takes the board state and stores it in an array for undo redo functionality
        if GameLogic.turn < len(
            GameLogic.board_states
        ):  # if we are in a state between undos and redos
            GameLogic.board_states = GameLogic.board_states[: GameLogic.turn]
            # we appned the current state and remove all future states that then become improbable futures
            GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))
            GameLogic.score_states = GameLogic.score_states[: GameLogic.turn]
            GameLogic.score_states.append(GameLogic.get_score_state())
            GameLogic.turn = len(GameLogic.board_states)
        else:
            GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))
            GameLogic.score_states.append(GameLogic.get_score_state())
            GameLogic.turn += 1

    @staticmethod
    def undo_board():
        if GameLogic.undo_is_possible():
            GameLogic.turn -= 1  # update turn number
            prev_board, prev_groups = GameLogic.make_board_from_state(
                GameLogic.board_states[GameLogic.turn - 1]
            )
            prev_score_state = GameLogic.score_states[GameLogic.turn - 1]

            # update board and score states
            GameLogic.set_scores_using(prev_score_state)
            GameLogic.board = prev_board
            GameLogic.all_groups = prev_groups
            GameLogic.flip_turn()  # flip the turn
            return True
        return False

    def undo_is_possible():
        return GameLogic.turn > 2

    def redo_is_possible():
        return GameLogic.turn < len(GameLogic.board_states)

    def redo_board():
        if GameLogic.redo_is_possible():  # same as undo but the other way around
            next_board, next_groups = GameLogic.make_board_from_state(
                GameLogic.board_states[GameLogic.turn]
            )
            next_score_state = GameLogic.score_states[GameLogic.turn]
            GameLogic.set_scores_using(next_score_state)
            GameLogic.board = next_board
            GameLogic.all_groups = next_groups
            GameLogic.flip_turn()
            GameLogic.turn += 1
            return True
        return False

    @staticmethod
    def reset_board():
        GameLogic.current_player = (
            GameLogic.player1
        )  # go back to the defualt start values for the game variables
        GameLogic.temp_captured = 0

        GameLogic.board_states = [
            None,
        ]
        GameLogic.board = []
        GameLogic.all_groups = []
        GameLogic.score_states = [None, {"p1": [0, 0], "p2": [0, 0]}]

        for i in range(7):  # repopulate the board with empty pieces
            GameLogic.board.append([])
            for j in range(7):
                GameLogic.board[i].append(
                    Piece(i, j, GameLogic.board, GameLogic.all_groups)
                )
        GameLogic.board_states.append(GameLogic.get_board_state(GameLogic.board))
        GameLogic.turn = len(GameLogic.board_states)

    @staticmethod
    def print_board(board):  # for testing
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
