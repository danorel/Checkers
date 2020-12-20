from copy import deepcopy

from client import Game


from .Heuristic import heuristic


def next_move(game: Game,
              depth,
              maximizing_player):
    optimal_move = None
    a = float('-inf')
    for move in game.get_possible_moves():
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

    return optimal_move


def _minimax(game: Game,
             depth,
             player_num,
             maximizing_player,
             alpha,
             beta):
    if depth == 0 or game.is_over():
        return heuristic(game=game,
                         player_num=maximizing_player)

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
            if beta <= alpha:
                break
        return value
