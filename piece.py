class Piece:
    def __init__(self, y, x, board):
        self.board = board
        self.y = y
        self.x = x
        self.type = 0  # 0 is emtpy / 1 is black / 2 is white
        self.liberties = None

        self.position_type = (
            self.find_position_type()
        )  # 0 is corner / 1 is edge / 2 is niether
        self.calculate_initial_liberties()

    def calculate_initial_liberties(self):
        if self.position_type == 0:
            self.liberties = 2
        elif self.position_type == 1:
            self.liberties = 3
        else:
            self.liberties = 4

    def find_position_type(self):
        if self.x not in [0, 6] and self.y not in [0, 6]:
            return 2  # neither edge nor corner
        if self.x in [0, 6] and self.y in [0, 6]:
            return 0  # corner
        return 1

    def calculate_liberties(self):
        neighbours = self.get_neighbours()
        for neighbour in neighbours:
            if neighbour.type != 0:
                self.liberties -= 1

        return self.liberties

    def get_neighbours(self):
        x = self.x
        y = self.y

        pos = [(y + 1, x), (y, x + 1), (y - 1, x), (y, x - 1)]

        pos[:] = [
            neighbour
            for neighbour in pos
            if not (neighbour[0] in [-1, 7] or neighbour[1] in [-1, 7])
        ]

        neighbours = []

        for position in pos:
            neighbours.append(self.board[position[0]][position[1]])

        return neighbours
