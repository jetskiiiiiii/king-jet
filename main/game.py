import pygame
import os
import numpy as np
from typing import List, Optional, Tuple

from resources.ui import *
from pieces import *
from board import *

pygame.init()
screen = pygame.display.set_mode((13*tile_size, 8*tile_size))
clock = pygame.time.Clock()
running = True

dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


pieces_array = [
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


chessboard = Board() 

# Outside of MAIN loop because need to be remembered
clicked_piece: Piece | None = None
reset_squares_at_these_coors = []

## Main pygame loop
while running:
    event_list = pygame.event.get()
    screen.fill(background)

    ## Render chess pieces
    chessboard.draw_pieces_start(pieces_array)
    ## Draw chess board
    screen.blit(chessboard.board_surface, (0, 0))

    for event in event_list:
        dirty_rects = []
        if event.type == pygame.QUIT:
            running = False
        ## get_pressed returns either 3 or 5 buttons
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            # Detect if piece has been clicked 
            
            if len(reset_squares_at_these_coors) > 0:
                dirty_rects = chessboard.remove_piece_hints(reset_squares_at_these_coors) 
                reset_squares_at_these_coors = []
                pygame.display.update(dirty_rects)

            new_clicked_piece: Piece | None = None
            for piece in pieces_array:
                # TODO: Prevent calculating if same piece is clicked
                if piece.current_hitbox.collidepoint(mouse_pos) and (not piece.is_clicked):
                    new_clicked_piece = piece
                    piece.is_clicked = True
                    hints, reset_squares_at_these_coors = chessboard.draw_piece_hints(piece)
                    # print(reset_squares_at_these_coors)
                    dirty_rects = hints
                    pygame.display.update(dirty_rects)
                    break # If piece was clicked, break loop
            # If clicked piece didn't change, there was a click on an empty square
            if (new_clicked_piece is None) and (clicked_piece is not None):
                dirty_rects = chessboard.move_piece(mouse_pos, clicked_piece)
                pygame.display.update(dirty_rects)
                clicked_piece = None
            else:
                clicked_piece = new_clicked_piece # If the new clicked piece is different than the last, the user has decided to change piece they want to move

            # Detect if mouse click 1) after clicking piece 2) on a legal move or on another piece

    pygame.display.update()
    clock.tick(60)

pygame.quit()
