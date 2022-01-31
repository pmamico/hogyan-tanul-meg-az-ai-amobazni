from IPython.display import HTML, display, clear_output
from tic_tac_toe.Jatekos import Jatekos
from tic_tac_toe.Tabla import Tabla, JatekEredmeny, X, O
import numpy as np
import pandas as pd
import time


def mutasd_meg(tabla):
  clear_output(wait=True)
  print(pd.DataFrame(np.array(tabla.state_to_charlist())))


def play_game(tabla: Tabla, player1: Jatekos, player2: Jatekos, silent: bool = True):
    player1.uj_jatek(X)
    player2.uj_jatek(O)
    tabla.torles()

    finished = False
    while not finished:
        result, finished = player1.lepj(tabla)
        if finished:
            if result == JatekEredmeny.DONTETLEN:
                final_result = JatekEredmeny.DONTETLEN
            else:
                final_result = JatekEredmeny.X_NYERT
        else:
            result, finished = player2.lepj(tabla)
            if finished:
                if result == JatekEredmeny.DONTETLEN:
                    final_result = JatekEredmeny.DONTETLEN
                else:
                    final_result = JatekEredmeny.O_NYERT

    # noinspection PyUnboundLocalVariable
    player1.vegeredmeny(final_result)
    # noinspection PyUnboundLocalVariable
    player2.vegeredmeny(final_result)
    return final_result

def elo_jatek(tabla: Tabla, player1: Jatekos, player2: Jatekos):
    player1.uj_jatek(X)
    player2.uj_jatek(O)
    tabla.torles()
    mutasd_meg(tabla)
    finished = False
    while not finished:
        time.sleep(1)
        result, finished = player1.lepj(tabla)
        mutasd_meg(tabla)
        if finished:
            if result == JatekEredmeny.DONTETLEN:
                final_result = JatekEredmeny.DONTETLEN
            else:
                final_result = JatekEredmeny.X_NYERT
        else:
            time.sleep(1)
            result, finished = player2.lepj(tabla)
            mutasd_meg(tabla)
            if finished:
                if result == JatekEredmeny.DONTETLEN:
                    final_result = JatekEredmeny.DONTETLEN
                else:
                    final_result = JatekEredmeny.O_NYERT

    # noinspection PyUnboundLocalVariable
    player1.vegeredmeny(final_result)
    # noinspection PyUnboundLocalVariable
    player2.vegeredmeny(final_result)
    return final_result


def battle(player1: Jatekos, player2: Jatekos, num_games: int = 100000, silent: bool = False):
    tabla = Tabla()
    draw_count = 0
    cross_count = 0
    naught_count = 0
    for _ in range(num_games):
        result = play_game(tabla, player1, player2)
        if result == JatekEredmeny.X_NYERT:
            cross_count += 1
        elif result == JatekEredmeny.O_NYERT:
            naught_count += 1
        else:
            draw_count += 1

    if not silent:
        print("After {} game we have draws: {}, Player 1 wins: {}, and Player 2 wins: {}.".format(num_games, draw_count,
                                                                                                  cross_count,
                                                                                                  naught_count))

        print("Which gives percentages of draws: {:.2%}, Player 1 wins: {:.2%}, and Player 2 wins:  {:.2%}".format(
            draw_count / num_games, cross_count / num_games, naught_count / num_games))

    return cross_count, naught_count, draw_count
