#
# based on Carsten Friedrichs tic-tac-toe 
# reimplemented by Mico Papp
#

from tic_tac_toe.Tabla import Tabla, URES, JatekEredmeny
from tic_tac_toe.Jatekos import Jatekos


class MiniMaxRobot(Jatekos):
    """
    A computer player implementing the Min Max algorithm.

    This player behaves deterministically. That is, for a given tabla position the player will always make the same
    move, even if other moves with the same evaluation exist.

    Already evaluated tabla positions are cached for efficiency.
    """

    WIN_VALUE = 1
    DRAW_VALUE = 0
    LOSS_VALUE = -1

    def __init__(self):
        """
        Getting ready for playing tic tac toe.
        """
        self.side = None
        """
        Cache to store the evaluation of tabla positions that we have already looked at. This avoids repeating a lot
        of work as we do not look at all the possible continuation from this position again.
        """
        self.cache = {}
        super().__init__()

    def uj_jatek(self, side: int):
        """
        Setting the side for the game to come. Noting else to do.
        :param side: The side this player will be playing
        """
        if self.side != side:
            self.side = side
            self.cache = {}

    def vegerendmeny(self, result: JatekEredmeny):
        """
        Does nothing.
        :param result: The result of the game that just finished
        :return:
        """
        pass

    def _min(self, tabla: Tabla) -> (float, int):
        """
        Evaluate the tabla position `tabla` from the Minimizing player's point of view.

        :param tabla: The tabla position to evaluate
        :return: Tuple of (Best Result, Best Move in this situation). Returns -1 for best move if the game has already
        finished
        """

        #
        # First we check if we have seen this tabla position before, and if yes just return the cached value
        #
        tabla_hash = tabla.hash_value()
        if tabla_hash in self.cache:
            return self.cache[tabla_hash]

        #
        # Init the min value as well as action. Min value is set to DONTETLEN as this value will pass through in case
        # of a draw
        #
        min_value = self.DRAW_VALUE
        action = -1

        #
        # If the game has already finished we return. Otherwise we look at possible continuations
        #
        winner = tabla.who_won()
        if winner == self.side:
            min_value = self.WIN_VALUE
            action = -1
        elif winner == tabla.other_side(self.side):
            min_value = self.LOSS_VALUE
            action = -1
        else:
            for index in [i for i, e in enumerate(tabla.state) if tabla.state[i] == URES]:
                b = Tabla(tabla.state)
                b.lepj(index, tabla.other_side(self.side))

                res, _ = self._max(b)
                if res < min_value or action == -1:
                    min_value = res
                    action = index

                    # Shortcut: Can't get better than that, so abort here and return this move
                    if min_value == self.LOSS_VALUE:
                        self.cache[tabla_hash] = (min_value, action)
                        return min_value, action

                self.cache[tabla_hash] = (min_value, action)
        return min_value, action

    def _max(self, tabla: Tabla) -> (float, int):
        """
        Evaluate the tabla position `tabla` from the Maximizing player's point of view.

        :param tabla: The tabla position to evaluate
        :return: Tuple of (Best Result, Best Move in this situation). Returns -1 for best move if the game has already
        finished
        """

        #
        # First we check if we have seen this tabla position before, and if yes just return the cached value
        #
        tabla_hash = tabla.hash_value()
        if tabla_hash in self.cache:
            return self.cache[tabla_hash]

        #
        # Init the min value as well as action. Min value is set to DONTETLEN as this value will pass through in case
        # of a draw
        #
        max_value = self.DRAW_VALUE
        action = -1

        #
        # If the game has already finished we return. Otherwise we look at possible continuations
        #
        winner = tabla.who_won()
        if winner == self.side:
            max_value = self.WIN_VALUE
            action = -1
        elif winner == tabla.other_side(self.side):
            max_value = self.LOSS_VALUE
            action = -1
        else:
            for index in [i for i, e in enumerate(tabla.state) if tabla.state[i] == URES]:
                b = Tabla(tabla.state)
                b.lepj(index, self.side)

                res, _ = self._min(b)
                if res > max_value or action == -1:
                    max_value = res
                    action = index

                    # Shortcut: Can't get better than that, so abort here and return this move
                    if max_value == self.WIN_VALUE:
                        self.cache[tabla_hash] = (max_value, action)
                        return max_value, action

                self.cache[tabla_hash] = (max_value, action)
        return max_value, action

    def lepj(self, tabla: Tabla) -> (JatekEredmeny, bool):
        """
        Making a move according to the MinMax algorithm

        :param tabla: The tabla to make a move on
        :return: The result of the move
        """
        score, action = self._max(tabla)
        _, res, finished = tabla.lepj(action, self.side)
        return res, finished
