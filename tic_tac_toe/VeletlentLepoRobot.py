#
# based on Carsten Friedrichs tic-tac-toe 
# reimplemented by Mico Papp
#

from tic_tac_toe.Tabla import Tabla, JatekEredmeny
from tic_tac_toe.Jatekos import Jatekos


class VeletlentLepoRobot(Jatekos):
    """
    This player can play a game of Tic Tac Toe by randomly choosing a free spot on the tabla.
    It does not learn or get better.
    """

    def __init__(self):
        """
        Getting ready for playing tic tac toe.
        """
        self.side = None
        super().__init__()

    def lepj(self, tabla: Tabla) -> (JatekEredmeny, bool):
        """
        Making a random move
        :param tabla: The tabla to make a move on
        :return: The result of the move
        """
        _, res, finished = tabla.lepj(tabla.veletlen_ures_cella(), self.side)
        return res, finished

    def vegeredmeny(self, result: JatekEredmeny):
        """
        Does nothing.
        :param result: The result of the game that just finished
        :return:
        """
        pass

    def uj_jatek(self, side: int):
        """
        Setting the side for the game to come. Noting else to do.
        :param side: The side this player will be playing
        """
        self.side = side
