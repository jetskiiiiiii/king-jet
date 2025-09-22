import pygame
import numpy as np
import math
from typing import List, Optional, Tuple

from resources.ui import *
from resources.utils import *
from pieces import *

class Status():
    def __init__(self, quick_status: int, occupied: bool, hint: bool, attacked: bool, promotion: bool, occupied_by: Piece | None = None):
        #self.color = color # Color of square
        self.quick_status = quick_status # 0=empty, 1=occupied
        self.occupied = occupied
        self.hint = hint
        self.attacked = attacked
        self.promotion = promotion
        self.occupied_by = occupied_by

# Class to show status (graphically) of each square on board (empty, occupied, hint, attack, promotion)
class BoardStatus():
    def __init__(self):
        self.status = self.initialize_status()

    def __setitem__(self, key, value):
        self.status[key] = value

    def __getitem__(self, key):
        self.status[key]

    def initialize_status(self):
        status = []
        for col in range(0,8):
            for row in range(0,8):
                status.append(Status(quick_status=0, occupied=False, hint=False, attacked=False, promotion=False))
        return np.array(status).reshape(8,8)

    # Every time the graphic changes, update board status
    def change_status_of_square(self, position: Tuple, status: Status):
        self.status[position] = status
        return self.status

    # TODO: Not incorporated yet
    # Every time piece is clicked, change clicked attribute
    def change_click_of_square(self, position: Tuple):
        self.status[position].clicked = True

    def __str__(self):
        quick_status_only_array = []
        for row in range(0,8):
            for col in range(0,8):
                quick_status_only_array.append(self.status[col, row].quick_status)

        quick_status_only_array = np.array(quick_status_only_array).reshape(8,8)
        return f"{quick_status_only_array}"

# Class to hold game logic (turns, moves, pieces captured)
class BoardLogic():
    def __init__(self):
        self.turn = "light"
        self.toggle_move_piece = False
        self.moves = []
        self.pieces_captured_by_light = []
        self.pieces_captured_by_dark = []
        self.clicked_square = ()
        self.last_clicked_square = ()
        self.toggle_show_hints = False
        self.last_hints_shown = []
        self.pieces_array = [
            King("dark"),
            King("light"),

            Queen("dark"),
            Queen("light"),

            Bishop("dark", 0),
            Bishop("dark", 1),
            Bishop("light", 0),
            Bishop("light", 1),

            Knight("dark", 0),
            Knight("dark", 1),
            Knight("light", 0),
            Knight("light", 1),

            Rook("dark", 0),
            Rook("dark", 1),
            Rook("light", 0),
            Rook("light", 1),

            *[Pawn("dark", count) for count in range(8)],
            *[Pawn("light", count) for count in range(8)],
        ]

class Board():
    def __init__(self, screen: pygame.Surface, board_status: BoardStatus, board_logic: BoardLogic, tile_size: int = tile_size, dark_color: Tuple = dark_color, light_color: Tuple = light_color):
        self.screen = screen
        self.board_status = board_status
        self.board_logic = board_logic
        self.board_status_flat = board_status.status.ravel()
        self.tile_size = tile_size
        self.dark_color = dark_color
        self.light_color = light_color
        self.light_and_dark_arrangement = np.indices((8, 8)).sum(axis=0) % 2
        self.board_surface = pygame.Surface((8*self.tile_size, 8*self.tile_size))

    def get_center_coor(self, image_width, image_height):
        offset_width = self.tile_size - image_width
        offset_height = self.tile_size - image_height

        # col, row
        return offset_width / 2, offset_height / 2

    def scale_piece(self, image, image_width, image_height):
        scale_by_width = self.tile_size // image_width
        scale_by_height = self.tile_size // image_height
        return pygame.transform.scale(image, (image_width * scale_by_width, image_height * scale_by_height))

    def is_click_inside_board(self, square_clicked: Tuple):
        return True if ((square_clicked[0] < 8) and (square_clicked[1] < 8)) else False

    # New drawing paradigm where every drawing creates at least a new square (with the option to overlay a piece/hint + change color of square)
    # Should receive info about location (which square), what to draw
    # Should have surface for every square color, piece, hint
    def draw_square(self, position: Tuple, color_type: str = "default", overlay: pygame.Surface | None = None):
        square_surface = pygame.Surface((self.tile_size, self.tile_size))

        color_dict = {"default": dark_color if self.light_and_dark_arrangement[position] else light_color,
                      "attack": attack_tile_color,
                      "promotion": promotion_tile_color}
        color = color_dict[color_type]
        square_surface.fill(color)

        if overlay is not None:
            center_pos_row, center_pos_col = self.get_center_coor(overlay.get_width(), overlay.get_height())
            square_surface.blit(overlay, (center_pos_col, center_pos_row))
        square_surface.set_colorkey(key_color)

        dirty_rect = self.board_surface.blit(square_surface, (position[0]*tile_size, position[1]*tile_size))
        self.screen.blit(self.board_surface, (0, 0))
        return dirty_rect

    ## Where pieces are placed onto the board
    def draw_pieces(self):
        for piece in self.board_logic.pieces_array:
            position = (piece.current_pos_col, piece.current_pos_row)
            self.draw_square(position, overlay = piece.image)
            self.board_status[position] = Status(quick_status=1, occupied=True, hint=True, attacked=False, promotion=False, occupied_by=piece)
        return None

    def fill_rest_of_board(self):
        for row in range(0, 8):
            for col in range(0, 8):
                if self.board_status.status[col, row].occupied == False:
                    self.draw_square((col, row))
        return None

    def draw_piece_hints(self):
        square_clicked = self.board_logic.clicked_square
        piece = self.board_status.status[square_clicked].occupied_by
        legal_moves, legal_attacks = self.get_legal_hints(piece)
        
        # TODO: PROGRAM LEGAL ATTACKS UI
        
        # Update board status/logic
        for hint in self.board_logic.last_hints_shown:
            self.board_status.status[hint].hint = False
            
        self.board_logic.last_hints_shown = []

        for move in legal_moves:
            overlay = Hint().hint_mark
            self.draw_square(position=move, overlay=overlay)

            # Update board status and logic
            self.board_status.status[move].hint = True
            self.board_logic.last_hints_shown.append(move)

        return None

    # Gets legal moves from piece rules + places restrains from surrounding pieces, board restrictions
    # TODO:
    # en peassant
    # Pins on king
    # Checks / checkmate
    def get_legal_hints(self, piece: Piece):
        # If player in check, only show moves that put player out of check
        #if self.player_in_check():
        
        # When piece is pinned to king or in check (and not one of pieces that move player out of check)
        #if self.piece_is_pinned():

        # occupied_by may be None
        if piece is None:
            return []

        initial_hints = piece.get_legal_moves()
        refined_hints, attack_hints, obstructions = [], [], [] # Will store slope + distance
        for move in initial_hints:
            vector = (move[0] - piece.current_pos_col, move[1] - piece.current_pos_row)
            angle = math.atan2(vector[1], vector[0])
            status_square_clicked = self.board_status.status[move]
            
            # If square is occupied, mark path as having obstructions, move to next square
            if (status_square_clicked.occupied):
                obstructions.append(angle)
                # If piece occupying square is opposite colored, piece can attack square
                if status_square_clicked.occupied_by.side != self.board_logic.turn:
                    attack_hints.append(angle)
                continue
            # If path has obstructions, move to next square
            # TODO: Make this more efficient by eliminating the entire angle 
            elif angle in obstructions:
                continue
            else:
                refined_hints.append(move)

            # TODO: Implement en peassant and king pin
            #if (piece.piece_type == "pawn"):
            #    self.check_en_passant(piece)
            #    continue
            #else:
            #refined_hints.append(move)

        return refined_hints, attack_hints


    # TODO: Implement move tracker
    def check_en_passant(self, piece: Piece):
        if piece.piece_type != "pawn":
            return False
        
    def move_piece(self):
        position = self.board_logic.clicked_square
        last_clicked_square = self.board_logic.last_clicked_square
        piece = self.board_status.status[last_clicked_square].occupied_by
        
        # Safeguarding in case occupied_by == None
        if piece:
            piece.current_pos_col = position[0]
            piece.current_pos_row = position[1]
        
        self.board_logic.last_hints_shown = []

        # Update board status/logic
        # Update quick_status, occupied, occupied_by
        self.board_status.status[last_clicked_square].quick_status = 0
        self.board_status.status[last_clicked_square].occupied = False
        self.board_status.status[last_clicked_square].occupied_by = None
        
        self.board_status.status[position].quick_status = 1
        self.board_status.status[position].occupied = True
        self.board_status.status[position].occupied_by = piece

        return None

class BlackTile():
    def __init__(self):
        self.color = dark_color

class LightTile():
    def __init__(self):
        self.color = light_color

class AttackTile():
    def __init__(self):
        self.color = attack_tile_color

class PromotionTile():
    def __init__(self):
        self.color = promotion_tile_color

class Hint():
    def __init__(self):
        self.color = background
        self.image_file_name = "resources/art/hint_mark.png"
        self.hint_mark = pygame.image.load(self.image_file_name).convert_alpha()

    def get_width(self):
        return self.hint_mark.get_width()

    def get_height(self):
        return self.hint_mark.get_height()
