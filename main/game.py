import pygame
import os
import numpy as np
from typing import List

pieces_image_path = "resources/art/"

pygame.init()
tile_size = 100
screen = pygame.display.set_mode((13*tile_size, 8*tile_size))
clock = pygame.time.Clock()
running = True

# Global values
dark_color = (76, 35, 10)
light_color = (165, 63, 43)
background = (204, 201, 161)
key_color = (128, 0, 128)
dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


class Pieces():
    def __init__(self, tile_size: int, name: str, piece_type: str, is_dark: bool, start_position_row: int, start_position_col: int, image_file_name: str):
        self.tile_size = tile_size
        self.name = name
        self.piece_type = piece_type
        self.is_dark = is_dark 
        self.image_file_name = image_file_name
        self.image = pygame.image.load(os.path.join(pieces_image_path, self.image_file_name)).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.start_position_row = start_position_row * self.tile_size
        self.start_position_col = start_position_col * self.tile_size

        ## Modified properties
        self.scaled_image = self.scale_piece()
        self.scaled_image_width = self.scaled_image.get_width()
        self.scaled_image_height = self.scaled_image.get_height()
        self.center_position_row, self.center_position_col = self.get_center_coor()

        ## Surface and its properties
        self.piece_surface = self.blit_image_to_square()

    def scale_piece(self):
        scale_by_width = self.tile_size // self.image_width
        scale_by_height = self.tile_size // self.image_height
        return pygame.transform.scale(self.image, (self.image_width * scale_by_width, self.image_height * scale_by_height))

    def get_center_coor(self):
        offset_width = self.tile_size - self.scaled_image_width
        offset_height = self.tile_size - self.scaled_image_height

        return offset_width / 2, offset_height / 2

    def blit_image_to_square(self):
        piece_surface = pygame.Surface((self.tile_size, self.tile_size))

        piece_surface.fill(key_color)
        piece_surface.blit(self.scaled_image, (self.center_position_col, self.center_position_row))
        piece_surface.set_colorkey(key_color)

        return piece_surface

    def move_piece(self):
        is_pressed = pygame.mouse.get_pressed(num_buttons=1)

## Create separate classes for each piece to set moving rules
class King(Pieces):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 4 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"
        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.image_file_name)

class Queen(Pieces):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 3 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"
        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.image_file_name)

class Bishop(Pieces):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool, count: int):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}_{count}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.count = count ## 0 is the left piece, 1 is the right piece
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 2 if (count == 0) else 5 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"
        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.image_file_name)

class Knight(Pieces):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool, count: int):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}_{count}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.count = count ## 0 is the left piece, 1 is the right piece
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 1 if (count == 0) else 6 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"
        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.image_file_name)

class Rook(Pieces):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool, count: int):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}_{count}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.count = count ## 0 is the left piece, 1 is the right piece
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 0 if (count == 0) else 7
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"
        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.image_file_name)

class Pawn(Pieces):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool, count: int):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}_{count}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.count = count ## Denotes which pawn, from 0 = most left to 8 = most right
        self.start_position_row = 1 if is_dark else 6
        self.start_position_col = count 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"
        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.image_file_name)


class Board():
    def __init__(self, tile_size: int, dark_color: tuple, light_color: tuple):
        self.tile_size = tile_size
        self.dark_color = dark_color
        self.light_color = light_color
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
    def draw_pieces_start(self, pieces: List[Pieces]):
        for piece in pieces:
            self.board_surface.blit(piece.piece_surface, (piece.start_position_col, piece.start_position_row))


pieces_array = [
    King(tile_size, "king", True),
    King(tile_size, "king", False),

    Queen(tile_size, "queen", True),
    Queen(tile_size, "queen", False),

    Bishop(tile_size, "bishop", True, 0),
    Bishop(tile_size, "bishop", True, 1),
    Bishop(tile_size, "bishop", False, 0),
    Bishop(tile_size, "bishop", False, 1),

    Knight(tile_size, "knight", True, 0),
    Knight(tile_size, "knight", True, 1),
    Knight(tile_size, "knight", False, 0),
    Knight(tile_size, "knight", False, 1),

    Rook(tile_size, "rook", True, 0),
    Rook(tile_size, "rook", True, 1),
    Rook(tile_size, "rook", False, 0),
    Rook(tile_size, "rook", False, 1),

    *[Pawn(tile_size, "pawn", True, count) for count in range(8)],
    *[Pawn(tile_size, "pawn", False, count) for count in range(8)],
]

## Main pygame loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(background)

    ## Render chess board
    chessboard = Board(tile_size, dark_color, light_color) 
    ## Render chess pieces
    chessboard.draw_pieces_start(pieces_array)
    ## Draw chess board
    screen.blit(chessboard.board_surface, (0, 0))

    clock.tick(60)

pygame.quit()
