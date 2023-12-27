class Piece(object):
    def __init__(self, y, x, board, all_groups):
        self.board = board
        self.y = y  # row
        self.x = x  # column
        self.type = 0  # 0 is emtpy / 1 is black / 2 is white
        self.liberties = (
            None  # liberties need to be calculated first based on piece position
        )
        self.all_groups = all_groups
        self.group = None

        self.position_type = (
            self.find_position_type()
        )  # 0 is corner / 1 is edge / 2 is niether
        self.calculate_initial_liberties()  # calculate liberties based on position type

    def calculate_initial_liberties(self):
        if self.position_type == 0:  # corner
            self.liberties = 2
        elif self.position_type == 1:  # edge
            self.liberties = 3
        else:
            self.liberties = 4  # middle roll

    def find_position_type(
        self,
    ):  # find the position tye based on the index of the piece
        if self.x not in [0, 6] and self.y not in [0, 6]:
            return 2  # neither edge nor corner
        if self.x in [0, 6] and self.y in [0, 6]:
            return 0  # corner
        return 1

    def calculate_liberties(
        self,
    ):  # calculate the liberties based on how many pieces surround it
        neighbours = (
            self.get_neighbours()
        )  # get the pieces that are directly around this piece
        for neighbour in neighbours:
            if (
                neighbour.type != 0
            ):  # if piece is not an empty piece then subtract one from the liberties
                self.liberties -= 1

        return self.liberties

    def get_neighbours(
        self,
    ):  # get the piece objects on the top bottom left and right of this piece
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

    def add_to_group(self):
        # finds neighbouring groups to add itself to or creates a new group on its own
        neighbour_groups = []
        neighbours = self.get_neighbours()

        # find all the unique neighbouring groups such that they are of the same type as this piece
        for piece in neighbours:
            if (
                piece.type == self.type
                and piece.group is not None
                and piece.group not in neighbour_groups
            ):
                neighbour_groups.append(piece.group)

        if (
            not neighbour_groups
        ):  # if no groups found then ccreate agroup for this piece alone
            group = Group(self.all_groups, self)
            return group
        else:
            if len(neighbour_groups) > 1:  # if more tha one group found
                for group in neighbour_groups[1:]:
                    neighbour_groups[0].merge(group)  # merge all the groups

            neighbour_groups[0].stones.append(
                self
            )  # else append this piece to the only neighboring group
            self.group = neighbour_groups[0]
            return neighbour_groups[0]

    def increment_neighbour_liberties(
        self,
    ):  # get all neighbouts and increment their libnerties (done when  a piece is taken off the board)
        neighbours = self.get_neighbours()
        for piece in neighbours:
            piece.liberties = piece.liberties + 1

    def decrement_neighbour_liberties(
        self,
    ):  # get all neighbours and decrement their liberties (done when a piece is placed on the board)
        neighbours = self.get_neighbours()
        for piece in neighbours:
            piece.liberties = piece.liberties - 1

    def place(self, type):  # set the type of the piece
        self.type = type

    def remove(self):  # set the piece to an empry piece
        self.type = 0
        self.group = None  # make it associated to none of the groups
        self.increment_neighbour_liberties()  # and increment neighbour liberties


class Group(object):
    def __init__(self, all_groups, stone):
        self.all_groups = all_groups  # list of lal groups on the board
        self.all_groups.append(self)  # append this group to the list
        self.stones = [stone]  # add the first stone in the group
        stone.group = self  # the group in which thhis stone is

    def merge(self, group):
        """Merge two groups.

        This method merges the argument group with this one by adding
        all its stones into this one. After that it removes the group
        from the board.

        Arguments:
        group -- the group to be merged with this one

        """
        for (
            stone
        ) in (
            group.stones
        ):  # move this groups stone is moved into the other group and this one is deleted
            stone.group = self
            self.stones.append(stone)
        self.all_groups.remove(group)
        del group

    def remove(self):
        """Remove the entire group."""
        try:
            counter = 0
            while (
                self.stones
            ):  # remove all the stones in this group and retrn the number of stones removed
                self.stones[0].remove()
                counter += 1
                del self.stones[0]
            self.all_groups.remove(self)
            return counter
        finally:
            del self

    def check_for_life(
        self,
    ):  # check if the group has any stones with any liberties still open
        for stone in self.stones:
            if stone.liberties > 0:
                return True
        return False
