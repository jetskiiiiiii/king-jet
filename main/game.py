import pygame
import os
import numpy as np
from typing import List, Optional, Tuple

from pygame.event import pump

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


class Piece():
    def __init__(self, tile_size: int, name: str, piece_type: str, is_dark: bool, start_position_row: int, start_position_col: int, current_pos_row: int, current_pos_col: int, legal_moves: List[Tuple], piece_range: int, image_file_name: str):
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
        self.current_hitbox = self.piece_surface.get_rect() # Scaled position
        self.is_clicked = False

        ## Legal moves
        self.current_pos_row = current_pos_row
        self.current_pos_col = current_pos_col
        self.legal_moves = legal_moves
        self.piece_range = piece_range

    def set_current_pos(self, new_pos: Tuple):
        self.current_pos_col = new_pos[0]
        self.current_pos_row = new_pos[1]
        return None
       
    def get_legal_moves(self):
        complete_legal_moves = []
        for step in range(self.piece_range):
            step += 1
            for move in self.legal_moves:
                direction = 1 if self.is_dark else -1
                x = self.current_pos_col + direction * (move[0] * step)
                y = self.current_pos_row + direction * (move[1] * step)
                # print(self.current_pos_row, move[1], step)
                # print(move, x, y)

                # If coords are outside of grid or is original position, don't add to possible moves
                if (x > 7) or (y > 7) or (x < 0) or (y < 0) or ((x, y) in complete_legal_moves) or ((x, y) == (self.current_pos_col, self.current_pos_row)):
                    continue
                complete_legal_moves.append((x, y))
        # print(complete_legal_moves)
        return complete_legal_moves 
        

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

## Create separate classes for each piece to set moving rules
class King(Piece):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 4 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_position_row
        self.current_pos_col = self.start_position_col
        self.legal_moves = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        self.piece_range = 1
        # x - 1, y + 1  top-left
        # x + 0, y + 1  top
        # x + 1, y + 1  top-right
        # x - 1, y      left
        # x + 1, y      right
        # x - 1, y - 1  bot-left
        # x + 0, y - 1  bot
        # x + 1, y - 1  bot-right

        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.current_pos_row, self.current_pos_col, self.legal_moves, self.piece_range, self.image_file_name)


class Queen(Piece):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 3 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_position_row
        self.current_pos_col = self.start_position_col
        self.legal_moves = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        self.piece_range = 8 

        # x - 1, y + 1  top-left
        # x + 0, y + 1  top
        # x + 1, y + 1  top-right
        # x - 1, y      left
        # x + 1, y      right
        # x - 1, y - 1  bot-left
        # x + 0, y - 1  bot
        # x + 1, y - 1  bot-right

        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.current_pos_row, self.current_pos_col, self.legal_moves, self.piece_range, self.image_file_name)

class Bishop(Piece):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool, count: int):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}_{count}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.count = count ## 0 is the left piece, 1 is the right piece
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 2 if (count == 0) else 5 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_position_row
        self.current_pos_col = self.start_position_col
        self.legal_moves = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
        self.piece_range = 8 

        # x - 1, y + 1  top-left
        # x + 1, y + 1  top-right
        # x - 1, y - 1  bot-left
        # x + 1, y - 1  bot-right

        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.current_pos_row, self.current_pos_col, self.legal_moves, self.piece_range, self.image_file_name)

class Knight(Piece):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool, count: int):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}_{count}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.count = count ## 0 is the left piece, 1 is the right piece
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 1 if (count == 0) else 6 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_position_row
        self.current_pos_col = self.start_position_col
        self.legal_moves = [(-2, 1), (-1, 2), (2, 1), (1, 2), (-2, -1), (-1, -2), (2, -1), (1, -2)]
        self.piece_range = 1

        # x - 2, y + 1  top-left-bot
        # x - 1, y + 2  top-left-top
        # x + 2, y + 1  top-right-bot
        # x + 1, y + 2  top-right-top
        # x - 2, y - 1  bot-left-top
        # x - 1, y - 2  bot-left-bot
        # x + 2, y - 1  bot-right-top
        # x + 1, y - 2  bot-right-bot

        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.current_pos_row, self.current_pos_col, self.legal_moves, self.piece_range, self.image_file_name)

class Rook(Piece):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool, count: int):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}_{count}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.count = count ## 0 is the left piece, 1 is the right piece
        self.start_position_row = 0 if is_dark else 7
        self.start_position_col = 0 if (count == 0) else 7
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_position_row
        self.current_pos_col = self.start_position_col
        self.legal_moves = [(0, 1), (-1, 0), (1, 0), (0, -1)]
        self.piece_range = 0

        # x + 0, y + 1  top
        # x - 1, y      left
        # x + 1, y      right
        # x + 0, y - 1  bot

        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.current_pos_row, self.current_pos_col, self.legal_moves, self.piece_range, self.image_file_name)

class Pawn(Piece):
    def __init__(self, tile_size: int, piece_type: str, is_dark: bool, count: int):
        self.tile_size = tile_size
        self.name = f"{piece_type}_{"dark" if is_dark else "light"}_{count}"
        self.piece_type = piece_type
        self.is_dark = is_dark
        self.count = count ## Denotes which pawn, from 0 = most left to 8 = most right
        self.start_position_row = 1 if is_dark else 6
        self.start_position_col = count 
        self.image_file_name = f"{piece_type}{1 if is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_position_row
        self.current_pos_col = self.start_position_col
        ## Pawns can only move forward, so black and white have different moves
        self.legal_moves = [(0, 1), (0, 2) if self.current_pos_row == self.start_position_row else (0, 1)] + [(-1, 1), (1, 1)]
        # self.legal_moves = [(move[0], move[1] * -1) if is_dark else move for move in self.legal_moves]
        self.piece_range = 1
        
        super().__init__(self.tile_size, self.name, piece_type, is_dark, self.start_position_row, self.start_position_col, self.current_pos_row, self.current_pos_col, self.legal_moves, self.piece_range, self.image_file_name)

class Board():
    def __init__(self, tile_size: int, dark_color: tuple, light_color: tuple):
        self.tile_size = tile_size
        self.dark_color = dark_color
        self.light_color = light_color
        self.light_and_dark_arrangement = np.indices((8, 8)).sum(axis=0) % 2
        self.board_surface = self.draw_board()


    # Left, top should already be to scale
    def get_center_of_square(self, pos: Tuple):
        left, top = pos[0], pos[1]
        return left + (tile_size // 2), top + (tile_size // 2)

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
            current_hitbox = self.board_surface.blit(piece.piece_surface, (piece.start_position_col, piece.start_position_row))
            piece.current_hitbox = current_hitbox

    def move_piece(self, mouse_pos: Tuple):
        # Getting position of the square clicked
        mouse_square_pos = (mouse_pos[0] // tile_size * tile_size, mouse_pos [1] // tile_size * tile_size)
        # TODO: Problem is what if the 2nd condition is met later in the list (situation where user changes mind and wants to move a different piece)
        for piece in pieces_array:
            if piece.is_clicked:
                piece.current_hitbox = self.board_surface.blit(piece.piece_surface, mouse_square_pos)
                dirty_rect = piece.current_hitbox

                piece.is_clicked = False
                return dirty_rect

    def draw_piece_hints(self, piece: Piece):
        legal_moves = piece.get_legal_moves()
        dirty_rects = []
        radius_of_hints = 10
        for move in legal_moves:
            scaled_move = scale_coor(move)
            centered_move = self.get_center_of_square(scaled_move)
            hint_mark = pygame.draw.circle(self.board_surface, background, centered_move, radius_of_hints) 
            dirty_rects.append(hint_mark)
        return dirty_rects, legal_moves

    def remove_piece_hints(self, coords_list: List[Tuple]):
        dirty_rects = []
        for coor in coords_list:
            scaled_coor = scale_coor(coor)
            color = light_color if self.light_and_dark_arrangement[coor[0]][coor[1]] else dark_color 
            rect = pygame.draw.rect(self.board_surface, color, pygame.Rect(scaled_coor, (tile_size, tile_size)))
            dirty_rects.append(rect)
        return dirty_rects

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

# To allow coordinates to be written on 8x8 grid and then here be converted to scale of actual board, based on tile size 
def scale_coor(coordinates: Tuple):
    return (tile_size * coordinates[0], tile_size * coordinates[1])

chessboard = Board(tile_size, dark_color, light_color) 
clicked_piece = Piece
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

            dirty_rects = chessboard.remove_piece_hints(reset_squares_at_these_coors) 
            pygame.display.update(dirty_rects)

            for piece in pieces_array:
                if piece.current_hitbox.collidepoint(mouse_pos):
                    clicked_piece = piece
                    piece.is_clicked = True
                    hints, reset_squares_at_these_coors = chessboard.draw_piece_hints(piece)
                    dirty_rects = hints
            # rect = chessboard.move_piece(mouse_pos)
            # dirty_rects.append(rect)
        pygame.display.update(dirty_rects)


    pygame.display.update()
    clock.tick(60)

pygame.quit()
