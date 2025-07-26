import pygame
import numpy as np
from typing import List, Optional, Tuple

from resources.ui import *
from resources.utils import *
from pieces import *

class Board():
    def __init__(self, tile_size: int = tile_size, dark_color: Tuple = dark_color, light_color: Tuple = light_color):
        self.tile_size = tile_size
        self.dark_color = dark_color
        self.light_color = light_color
        self.light_and_dark_arrangement = np.indices((8, 8)).sum(axis=0) % 2
        self.board_surface = self.draw_board()

    def draw_board(self):
        surface = pygame.Surface((8*self.tile_size, 8*self.tile_size))
        ## Render chess board
        row_count = 0
        ## Position is offset by the size of the tiles
        for row in range(0, 8*self.tile_size, self.tile_size):
            start_color = 0 if row_count % 2 == 0 else 1
            for col in range(0, 8*self.tile_size, 2*self.tile_size):
                ## If rows are even, start row with light, else start with dark
                surface.fill(dark_color, pygame.Rect((col+(start_color*self.tile_size), row), (self.tile_size, self.tile_size)))
                surface.fill(light_color, pygame.Rect((col+int(not start_color)*self.tile_size, row), (self.tile_size, self.tile_size)))
            row_count += 1

        return surface

    ## Where pieces are placed onto the board
    def draw_pieces_start(self, pieces: List[Piece]):
        for piece in pieces:
            current_hitbox = self.board_surface.blit(piece.piece_surface, (piece.start_pos_col, piece.start_pos_row))
            piece.current_hitbox = current_hitbox

    def move_piece(self, mouse_pos: Tuple, piece: Piece):
        # Getting position of the square clicked
        scaled_mouse_square_pos, unscaled_mouse_square_pos = get_square_that_was_clicked(mouse_pos, return_unscaled_square_coor = True)
        piece.current_hitbox = self.board_surface.blit(piece.piece_surface, scaled_mouse_square_pos)
        piece.is_clicked = False

        # Reset previous square that piece was on
        reset_rect = self.draw_empty_square_at_coor((piece.current_pos_col, piece.current_pos_row), piece_surface=None)

        # Update current position
        piece.current_pos_col = unscaled_mouse_square_pos[0] 
        piece.current_pos_row = unscaled_mouse_square_pos[1]

        # Rect that will be updated
        return piece.current_hitbox, reset_rect

    def draw_piece_hints(self, piece: Piece):
        legal_moves = piece.get_legal_moves()
        dirty_rects = []
        radius_of_hints = 10
        print(legal_moves)
        for move in legal_moves:
            scaled_move = scale_coor(move)
            centered_move = get_center_of_square(scaled_move)
            hint_mark = pygame.draw.circle(self.board_surface, background, centered_move, radius_of_hints) 
            dirty_rects.append(hint_mark)
        return dirty_rects, legal_moves

    def remove_piece_hints(self, coords_list: List[Tuple]):
        dirty_rects = []
        for coor in coords_list:
            dirty_rects.append(self.draw_empty_square_at_coor(coor))
        return dirty_rects
    
    def draw_empty_square_at_coor(self, coor: Tuple, piece_surface: pygame.Surface | None = None):
        # Put this rect into dirty_rects
        scaled_coor = scale_coor(coor)
        # print(coor, scaled_coor)
        color = light_color if self.light_and_dark_arrangement[coor[0]][coor[1]] else dark_color
        if piece_surface:
            return pygame.draw.rect(piece_surface, color, pygame.Rect(scaled_coor, (tile_size, tile_size)))
        return pygame.draw.rect(self.board_surface, color, pygame.Rect(scaled_coor, (tile_size, tile_size)))
