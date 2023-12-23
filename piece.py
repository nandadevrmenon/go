class Piece(object):
    def __init__(self, y, x, board, all_groups):
        self.board = board
        self.y = y
        self.x = x
        self.type = 0  # 0 is emtpy / 1 is black / 2 is white
        self.liberties = None
        self.all_groups = all_groups
        self.group = None

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

    def has_all_nieghbours_of_type(self, type):
        neighbours = self.get_neighbours()
        for neighbour in neighbours:
            if neighbour.type is not type:
                return False
        return True

    # def add_to_group(self):
    #     # finds neighbouring groups to add itself to ir creates a new group on its own
    #     neighbour_groups = []
    #     neighbours = self.get_neighbours()
    #     for piece in neighbours:
    #         if (
    #             piece.type == self.type
    #             and piece.group is not None
    #             and piece.group not in neighbour_groups
    #         ):
    #             neighbour_groups.append(piece.group)
    #     if not neighbour_groups:
    #         group = Group(self.board, self.all_groups, self)
    #         return group
    #     else:
    #         if len(neighbour_groups) > 1:
    #             for group in neighbour_groups[1:]:
    #                 neighbour_groups[0].merge(group)
    #         neighbour_groups[0].stones.append(self)
    #         return neighbour_groups[0]

    def add_to_group(self):
        # finds neighbouring groups to add itself to or creates a new group on its own
        neighbour_groups = []
        neighbours = self.get_neighbours()

        for piece in neighbours:
            if (
                piece.type == self.type
                and piece.group is not None
                and piece.group not in neighbour_groups
            ):
                neighbour_groups.append(piece.group)

        if not neighbour_groups:
            group = Group(self.board, self.all_groups, self)
            return group
        else:
            if len(neighbour_groups) > 1:
                for group in neighbour_groups[1:]:
                    neighbour_groups[0].merge(group)

            neighbour_groups[0].stones.append(self)
            self.group = neighbour_groups[0]
            return neighbour_groups[0]

    def remove(self):
        self.type = 0
        self.group = None

    def __str__(self):
        res = " " + str(self.y) + str(self.x)
        return res


class Group(object):
    def __init__(self, board, all_groups, stone):
        self.all_groups = all_groups
        self.all_groups.append(self)
        self.stones = [stone]
        stone.group = self

    def merge(self, group):
        """Merge two groups.

        This method merges the argument group with this one by adding
        all its stones into this one. After that it removes the group
        from the board.

        Arguments:
        group -- the group to be merged with this one

        """
        for stone in group.stones:
            stone.group = self
            self.stones.append(stone)
        self.all_groups.remove(group)
        del group

    def remove(self):
        """Remove the entire group."""
        while self.stones:
            self.stones[0].remove()
            del self.stones[0]
        self.all_groups.remove(self)
        del self

    def check_for_life(self):
        for stone in self.stones:
            if stone.liberties > 0:
                return True
        return False

    def __str__(self):
        """Return a list of the group's stones as a string."""
        return "".join(str(stone) for stone in self.stones)
