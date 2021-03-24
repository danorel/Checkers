import datetime
import logging
import random

from copy import deepcopy

from client import Game


from .heuristic import heuristic


def next_move(game: Game,
              depth,
              maximizing_player,
              available_time):
    logging.debug(f"Available time to move: {available_time}")
    # Calculate the terminate time.
    terminate_time = datetime.datetime.now() + datetime.timedelta(milliseconds=(available_time * 0.80) * 1000)
    logging.debug(f"Terminate date to next move: {terminate_time}")
    # Extract all available moves.
    available_moves = game.get_possible_moves()
    # Extract one random move for time-calculations safety.
    optimal_move = random.choice(available_moves)
    # Compare the time. If is ending - terminate the process.
    if datetime.datetime.now() > terminate_time:
        return optimal_move
    a = float('-inf')
    for move in available_moves:
        game_copy = deepcopy(game)
        game_copy.move(move)
        b = -_minimax(game=game_copy,
                      depth=depth - 1,
                      player_num=game_copy.whose_turn(),
                      maximizing_player=maximizing_player,
                      alpha=float('-inf'),
                      beta=float('+inf'))
        if a < b:
            a = b
            optimal_move = move

        if datetime.datetime.now() > terminate_time:
            return optimal_move

    return optimal_move


def _minimax(game: Game,
             depth,
             player_num,
             maximizing_player,
             alpha,
             beta):
    if depth == 0 or game.is_over():
        return heuristic(game=game,
                         player_turn=maximizing_player)

    if player_num == maximizing_player:
        value = float('-inf')
        for move in game.get_possible_moves():
            game_copy = deepcopy(game)
            game_copy.move(move)
            value = max(
                value,
                _minimax(game=game_copy,
                         depth=depth - 1,
                         player_num=game_copy.whose_turn(),
                         maximizing_player=maximizing_player,
                         alpha=alpha,
                         beta=beta))

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('+inf')
        for move in game.get_possible_moves():
            game_copy = deepcopy(game)
            game_copy.move(move)
            value = min(
                value,
                _minimax(game=game_copy,
                         depth=depth - 1,
                         player_num=game_copy.whose_turn(),
                         maximizing_player=maximizing_player,
                         alpha=alpha,
                         beta=beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value
