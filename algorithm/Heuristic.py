from client import Game


def heuristic(game: Game,
              player_num):
    pieces_ours = game.board.searcher.get_pieces_by_player(player_num)
    pieces_enemies = game.board.searcher.get_pieces_by_player(1 if player_num ==
                                                                 2 else 2)

    kings = filter(lambda p: p.king, pieces_ours)

    m_box = filter(
        lambda p: p.player == player_num and p.position in [14, 15, 18, 19],
        pieces_ours)
    m_rows = filter(
        lambda p: p.player == player_num and p.position in [13, 16, 17, 20],
        pieces_ours)

    if player_num == 1:
        back_row = filter(lambda p: p.position in [1, 2, 3, 4], pieces_ours)
    else:
        back_row = filter(lambda p: p.position in [29, 30, 31, 32], pieces_ours)

    # Finding the length of the pieces of both players
    pieces_ours, pieces_enemies = len(pieces_ours), len(pieces_enemies)

    kings, back_row = len(list(kings)), len(list(back_row))
    m_rows, m_box = len(list(m_rows)), len(list(m_box))

    return - (6 * pieces_ours - 1 * pieces_enemies + 6.75 * kings + 5 * back_row +
             2.5 * m_box + 0.5 * m_rows)
