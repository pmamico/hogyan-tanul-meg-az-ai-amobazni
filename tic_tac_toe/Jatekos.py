#
# based on Carsten Friedrichs tic-tac-toe 
# reimplemented by Mico Papp
#
from abc import ABC, abstractmethod

from tic_tac_toe.Tabla import Tabla, JatekEredmeny


class Jatekos(ABC):
    """
    Abstract class defining the interface we expect any Tic Tac Toe player class to implement.
    This will allow us to pit various different implementation against each other
    """

    def __init__(self):
        """
        Nothing to do here apart from calling our super class
        """
        super().__init__()

    @abstractmethod
    def lepj(self, tabla: Tabla) -> (JatekEredmeny, bool):
        """
        The player should make a move on tabla `tabla` and return the result. The return result can usually
        be passed on from the corresponding method in the tabla class.
        :param tabla: The tabla to make a move on
        :return: The JatekEredmeny after this move, Flag to indicate whether the move finished the game
        """
        pass

    #@abstractmethod
    def vegeredmeny(self, result: JatekEredmeny):
        """
        This method will be called after the game has finished. It allows the player to ponder its game move choices
        and learn from the experience
        :param result: The result of the game
        """
        pass

    @abstractmethod
    def uj_jatek(self, side: int):
        """
        This method will be called before a game starts. It allows the players to get ready for the game and also tells
        which side it is on.
        :param side: The side the player will play in the new game
        """
        pass
