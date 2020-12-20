class Heuristic:
    def __init__(self,
                 cof_dif_pawns=0,
                 cof_dif_kings=0,
                 cof_dif_on_edge_pawn=0,
                 cof_dif_on_edge_king=0,
                 cof_dif_defend_pieces=0,
                 cof_dif_on_top_three=0,
                 cof_dif_center_king=0,
                 cof_dif_center_pawn=0,
                 cof_dif_triangle=0,
                 cof_dif_bridge=0,
                 cof_dif_dog=0,
                 cof_dif_oreo=0,
                 cof_dif_kings_corner=0):
        self.cof_dif_pawns = cof_dif_pawns
        self.cof_dif_kings = cof_dif_kings
        self.cof_dif_on_edge_pawn = cof_dif_on_edge_pawn
        self.cof_dif_on_edge_king = cof_dif_on_edge_king
        self.cof_dif_defend_pieces = cof_dif_defend_pieces
        self.cof_dif_on_top_three = cof_dif_on_top_three
        self.cof_dif_center_king = cof_dif_center_king
        self.cof_dif_center_pawn = cof_dif_center_pawn
        self.cof_dif_triangle = cof_dif_triangle
        self.cof_dif_bridge = cof_dif_bridge
        self.cof_dif_dog = cof_dif_dog
        self.cof_dif_oreo = cof_dif_oreo
        self.cof_dif_kings_corner = cof_dif_kings_corner

    def count_heuristic(self,
                        num_dif_pawns,
                        num_dif_kings,
                        num_dif_on_edge_pawn,
                        num_dif_on_edge_king,
                        num_dif_defend_pieces,
                        num_dif_on_top_three,
                        num_dif_center_king,
                        num_dif_center_pawn,
                        dif_triangle,
                        dif_bridge,
                        dif_dog,
                        dif_oreo,
                        dif_kings_corner):
        heuristic = 0
        heuristic += self.cof_dif_pawns * num_dif_pawns
        heuristic += self.cof_dif_kings * num_dif_kings
        heuristic += self.cof_dif_on_edge_pawn * num_dif_on_edge_pawn
        heuristic += self.cof_dif_on_edge_king * num_dif_on_edge_king
        heuristic += self.cof_dif_defend_pieces * num_dif_defend_pieces
        heuristic += self.cof_dif_center_king * num_dif_center_king
        heuristic += self.cof_dif_on_top_three * num_dif_on_top_three
        heuristic += self.cof_dif_center_pawn * num_dif_center_pawn
        heuristic += self.cof_dif_triangle * dif_triangle
        heuristic += self.cof_dif_bridge * dif_bridge
        heuristic += self.cof_dif_dog * dif_dog
        heuristic += self.cof_dif_oreo * dif_oreo
        heuristic += self.cof_dif_kings_corner * dif_kings_corner
        return heuristic
