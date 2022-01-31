#
# based on Carsten Friedrichs tic-tac-toe 
# reimplemented by Mico Papp
#

import numpy as np
from enum import Enum


class JatekEredmeny(Enum):
    """
    Enum to encode different states of the game. A game can be in progress (BEFEJEZETLEN), lost, won, or draw
    """
    BEFEJEZETLEN = 0
    O_NYERT = 1
    X_NYERT = 2
    DONTETLEN = 3


#
# Values to encode the current content of a field on the tabla. A field can be empty, contain a naught, or
# contain a cross
#
URES = 0  # type: int
O = 1  # type: int
X = 2  # type: int

#
# Define the length and width of the tabla. Has to be 3 at the moment, or some parts of the code will break. Also,
# the game mechanics kind of require this dimension unless other rules are changed as well. Encoding as a variable
# to make the code more readable
#
BOARD_DIM = 3  # type: int
BOARD_SIZE = BOARD_DIM * BOARD_DIM  # type: int


class Tabla:
    """
    The class to encode a tic-tac-toe tabla, including its current state of pieces.
    Also contains various utility methods.
    """

    #
    # We will use these starting positions and directions when checking if a move resulted in the game being
    # won by one of the sides.
    #
    WIN_CHECK_DIRS = {0: [(1, 1), (1, 0), (0, 1)],
                      1: [(1, 0)],
                      2: [(1, 0), (1, -1)],
                      3: [(0, 1)],
                      6: [(0, 1)]}

    def hash_value(self) -> int:
        """
        Encode the current state of the game (tabla positions) as an integer. Will be used for caching evaluations
        :return: A collision free hash value representing the current tabla state
        """
        res = 0
        for i in range(BOARD_SIZE):
            res *= 3
            res += self.state[i]

        return res

    @staticmethod
    def other_side(side: int) -> int:
        """
        Utility method to return the value of the other player than the one passed as input
        :param side: The side we want to know the opposite of
        :return: The opposite side to the one passed as input
        """
        if side == URES:
            raise ValueError("URES has no 'other side'")

        if side == X:
            return O

        if side == O:
            return X

        raise ValueError("{} is not a valid side".format(side))

    def __init__(self, s=None):
        """
        Create a new Tabla. If a state is passed in, we use that otherwise we initialize with an empty tabla
        :param s: Optional tabla state to initialise the tabla with
        """
        if s is None:
            self.state = np.ndarray(shape=(1, BOARD_SIZE), dtype=int)[0]
            self.torles()
        else:
            self.state = s.copy()

    def coord_to_pos(self, coord: (int, int)) -> int:
        """
        Converts a 2D tabla position to a 1D tabla position.
        Various parts of code prefer one over the other.
        :param coord: A tabla position in 2D coordinates
        :return: The same tabla position in 1D coordinates
        """
        return coord[0] * BOARD_DIM + coord[1]

    def pos_to_coord(self, pos: int) -> (int, int):
        """
        Converts a 1D tabla position to a 2D tabla position.
        Various parts of code prefer one over the other.
        :param pos: A tabla position in 1D coordinates
        :return: The same tabla position in 2D coordinates
        """
        return pos // BOARD_DIM, pos % BOARD_DIM

    def torles(self):
        """
        Resets the game tabla. All fields are set to be URES.
        """
        self.state.fill(URES)

    def num_empty(self) -> int:
        """
        Counts and returns the number of empty fields on the tabla.
        :return: The number of empty fields on the tabla
        """
        return np.count_nonzero(self.state == URES)

    def veletlen_ures_cella(self) -> int:
        """
        Returns a random empty spot on the tabla in 1D coordinates
        :return: A random empty spot on the tabla in 1D coordinates
        """
        index = np.random.randint(self.num_empty())
        for i in range(9):
            if self.state[i] == URES:
                if index == 0:
                    return i
                else:
                    index = index - 1

    def is_legal(self, pos: int) -> bool:
        """
        Tests whether a tabla position can be played, i.e. is currently empty
        :param pos: The tabla position in 1D that is to be checked
        :return: Whether the position can be played
        """
        return (0 <= pos < BOARD_SIZE) and (self.state[pos] == URES)

    def lepj(self, position: int, side: int) -> (np.ndarray, JatekEredmeny, bool):
        """
        Places a piece of side "side" at position "position". The position is to be provided as 1D.
        Throws a ValueError if the position is not URES
        returns the new state of the tabla, the game result after this move, and whether this move has finished the game

        :param position: The position where we want to put a piece
        :param side: What piece we want to play (O, or X)
        :return: The game state after the move, The game result after the move, Whether the move finished the game
        """
        if self.state[position] != URES:
            print('Illegal move')
            raise ValueError("Invalid move")

        self.state[position] = side

        if self.check_win():
            return self.state, JatekEredmeny.X_NYERT if side == X else JatekEredmeny.O_NYERT, True

        if self.num_empty() == 0:
            return self.state, JatekEredmeny.DONTETLEN, True

        return self.state, JatekEredmeny.BEFEJEZETLEN, False

    def apply_dir(self, pos: int, direction: (int, int)) -> int:
        """
        Applies 2D direction dir to 1D position pos.
        Returns the resulting 1D position, or -1 if the resulting position would not be a valid tabla position.
        Used internally to check whether either side has won the game.
        :param pos: What position in 1D to apply the direction to
        :param direction: The direction to apply in 2D
        :return: The resulting 1D position, or -1 if the resulting position would not be a valid tabla position.
        """
        row = pos // 3
        col = pos % 3
        row += direction[0]
        if row < 0 or row > 2:
            return -1
        col += direction[1]
        if col < 0 or col > 2:
            return -1

        return row * 3 + col

    def check_win_in_dir(self, pos: int, direction: (int, int)) -> bool:
        """
        Checks and returns whether there are 3 pieces of the same side in a row if following direction dir
        Used internally to check whether either side has won the game.
        :param pos: The position in 1D from which to check if we have 3 in a row
        :param direction: The direction in 2D in which to check for 3 in a row
        :return: Whether there are 3 in a row of the same side staring from position pos and going in direction
        `direction`
        """
        c = self.state[pos]
        if c == URES:
            return False

        p1 = int(self.apply_dir(pos, direction))
        p2 = int(self.apply_dir(p1, direction))

        if p1 == -1 or p2 == -1:
            return False

        if c == self.state[p1] and c == self.state[p2]:
            return True

        return False

    def who_won(self) -> int:
        """
        Check whether either side has won the game and return the winner
        :return: If one player has won, that player; otherwise URES
        """
        for start_pos in self.WIN_CHECK_DIRS:
            if self.state[start_pos] != URES:
                for direction in self.WIN_CHECK_DIRS[start_pos]:
                    res = self.check_win_in_dir(start_pos, direction)
                    if res:
                        return self.state[start_pos]

        return URES

    def check_win(self) -> bool:
        """
        Check whether either side has won the game
        :return: Whether a side has won the game
        """
        for start_pos in self.WIN_CHECK_DIRS:
            if self.state[start_pos] != URES:
                for direction in self.WIN_CHECK_DIRS[start_pos]:
                    res = self.check_win_in_dir(start_pos, direction)
                    if res:
                        return True

        return False

    def state_to_char(self, pos, html=False):
        """
        Return 'x', 'o', or ' ' depending on what piece is on 1D position pos. Ig `html` is True,
        return '&ensp' instead of ' ' to enforce a white space in the case of HTML output
        :param pos: The position in 1D for which we want a character representation
        :param html: Flag indicating whether we want an ASCII (False) or HTML (True) character
        :return: 'x', 'o', or ' ' depending on what piece is on 1D position pos. Ig `html` is True,
        return '&ensp' instead of ' '
        """
        if (self.state[pos]) == URES:
            return '&ensp;' if html else ' '

        if (self.state[pos]) == O:
            return 'o'

        return 'x'

    def html_str(self) -> str:
        """
        Format and return the game state as a HTML table
        :return: The game state as a HTML table string
        """
        data = self.state_to_charlist(True)
        html = '<table border="1"><tr>{}</tr></table>'.format(
            '</tr><tr>'.join(
                '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
        )
        return html

    def state_to_charlist(self, html=False):
        """
        Convert the game state to a list of list of strings (e.g. for creating a HTML table view of it).
        Useful for displaying the current state of the game.
        :param html: Flag indicating whether we want an ASCII (False) or HTML (True) character
        :return: A list of lists of character representing the game state.
        """
        res = []
        for i in range(3):
            line = [self.state_to_char(i * 3, html),
                    self.state_to_char(i * 3 + 1, html),
                    self.state_to_char(i * 3 + 2, html)]
            res.append(line)

        return res

    def __str__(self) -> str:
        """
        Return ASCII representation of the tabla
        :return: ASCII representation of the tabla
        """
        tabla_str = ""
        for i in range(3):
            tabla_str += self.state_to_char(i * 3) + '|' + self.state_to_char(i * 3 + 1) \
                         + '|' + self.state_to_char(i * 3 + 2) + "\n"

            if i != 2:
                tabla_str += "-----\n"

        tabla_str += "\n"
        return tabla_str

    def mutasd_meg(self):
        """
        Print an ASCII representation of the tabla
        """
        for i in range(3):
            tabla_str = self.state_to_char(i * 3) + '|' + self.state_to_char(i * 3 + 1) \
                        + '|' + self.state_to_char(i * 3 + 2)

            print(tabla_str)
            if i != 2:
                print("-----")

        print("")
