from client import Game


def on_position_white(game, i):
    piece = game.board.searcher.get_piece_by_position(i)
    if piece is None:
        return False
    return piece.player == 1


def on_position_black(game, i):
    piece = game.board.searcher.get_piece_by_position(i)
    if piece is None:
        return False
    return piece.player == 2


# White on 1 2 6 / Black on 27 31 32
def heuristic_triangle(game, player_turn):
    if player_turn == 1:
        return on_position_white(game, 1) and on_position_white(game, 2) and on_position_white(game, 6)

    return on_position_black(game, 27) and on_position_black(game, 31) and on_position_black(game, 32)


# White on 2 3 7 / Black on 26 30 31
def heuristic_oreo(game, player_turn):
    if player_turn == 1:
        return on_position_white(game, 2) and on_position_white(game, 3) and on_position_white(game, 7)

    return on_position_black(game, 26) and on_position_black(game, 30) and on_position_black(game, 31)


# White on 1 3 / Black on 30, 32
def heuristic_bridge(game, player_turn):
    if player_turn == 1:
        return on_position_white(game, 1) and on_position_white(game, 3)

    return on_position_black(game, 30) and on_position_black(game, 32)


# White on 1 black on 5/ black on 32 white on 28
def heuristic_dog(game, player_turn):
    if player_turn == 1:
        return on_position_white(game, 1) and on_position_black(game, 5)

    return on_position_white(game, 28) and on_position_black(game, 32)


# White king on 29/ black king on 4
def heuristic_king_in_corner(game, player_turn):
    if player_turn == 1:
        piece = game.board.searcher.get_piece_by_position(29)
        if piece is None:
            return False
        return piece.player == 1 and piece.king
    else:
        piece = game.board.searcher.get_piece_by_position(4)
        if piece is None:
            return False
        return piece.player == 2 and piece.king


# White/Black kings amount of our pieces
def heuristic_king_amount(pieces_ours):
    return len(list(filter(lambda p: p.king, pieces_ours)))


# White/Black middle box amount of our pieces
def heuristic_middle_box(pieces_ours, player_turn):
    return len(list(filter(
        lambda p: p.player == player_turn and p.position in [14, 15, 18, 19],
        pieces_ours)))


# White/Black middle corner rows amount of our pieces
def heuristic_middle_rows(pieces_ours, player_turn):
    return len(list(filter(
        lambda p: p.player == player_turn and p.position in [13, 16, 17, 20],
        pieces_ours)))


# White/Black back rows amount of our pieces
def heuristic_back_rows(pieces_ours, player_turn):
    if player_turn == 1:
        return len(list(filter(lambda p: p.position in [1, 2, 3, 4], pieces_ours)))
    else:
        return len(list(filter(lambda p: p.position in [29, 30, 31, 32], pieces_ours)))


# White/Black amount of our pieces
def heuristic_pieces_ours(pieces_ours):
    return len(pieces_ours)


# White/Black amount of enemy pieces
def heuristic_pieces_enemies(pieces_enemies):
    return len(pieces_enemies)


def heuristic(game: Game,
              player_turn):
    pieces_ours = game.board.searcher.get_pieces_by_player(player_turn)
    pieces_enemies = game.board.searcher.get_pieces_by_player(1 if player_turn == 2
                                                                else 2)

    return - (3    * heuristic_pieces_ours(pieces_ours) -
              1    * heuristic_pieces_enemies(pieces_enemies) +
              5    * heuristic_king_amount(pieces_ours) +
              2    * heuristic_back_rows(pieces_ours, player_turn) +
              1.5  * heuristic_middle_box(pieces_ours, player_turn) +
              1    * heuristic_middle_rows(pieces_ours, player_turn) +
              0.25 * heuristic_king_in_corner(game, player_turn))
