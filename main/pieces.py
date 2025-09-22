import pygame
import os
from typing import List, Optional, Tuple

from resources.ui import *

pieces_image_path = "resources/art/"

class Piece():
    def __init__(self,
                 piece_type: str, 
                 side: str, 
                 is_dark: bool,
                 is_light: bool,
                 start_pos_row: int, 
                 start_pos_col: int, 
                 current_pos_row: int, 
                 current_pos_col: int, 
                 legal_moves: List[Tuple], 
                 piece_range: int, 
                 image_file_name: str, 
                 count: int | None = None,
                 tile_size: int = tile_size):
        
        self.tile_size = tile_size
        self.count = count
        self.piece_type = piece_type

        self.side = side
        self.is_dark = is_dark
        self.is_light = is_light

        self.name = f"{piece_type}_{"dark" if self.is_dark else "light"}{f"_{count}" if (self.count is not None) else ""}"

        self.image_file_name = image_file_name
        self.image_prescale = pygame.image.load(os.path.join(pieces_image_path, self.image_file_name)).convert_alpha()
        self.image_prescale_width = self.image_prescale.get_width()
        self.image_prescale_height = self.image_prescale.get_height()
        self.start_pos_row = start_pos_row
        self.start_pos_col = start_pos_col

        ## Modified properties
        self.image = self.scale_piece()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #self.center_pos_row, self.center_pos_col = self.get_center_coor()

        ## Surface and its properties
        # self.piece_surface = self.blit_image_to_square()
        # self.current_hitbox = self.piece_surface.get_rect() # Scaled position
        # self.is_clicked = False

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
        #print(self.name)
        for step in range(self.piece_range):
            step += 1
            for move in self.legal_moves:
                direction = 1 if self.is_dark else -1
                x = self.current_pos_col + direction * (move[0] * step)
                y = self.current_pos_row + direction * (move[1] * step)
                # print(self.current_pos_row, direction, move[1], step)
                # print(move, x, y)

                # If coords are outside of grid or is original position, don't add to possible moves
                if (x > 7) or (y > 7) or (x < 0) or (y < 0) or ((x, y) in complete_legal_moves) or ((x, y) == (self.current_pos_col, self.current_pos_row)):
                    continue
                complete_legal_moves.append((x, y))
        # print(complete_legal_moves)
        return complete_legal_moves 

    def scale_piece(self):
        scale_by_width = self.tile_size // self.image_prescale_width
        scale_by_height = self.tile_size // self.image_prescale_height
        return pygame.transform.scale(self.image_prescale, (self.image_prescale_width * scale_by_width, self.image_prescale_height * scale_by_height))


## Create separate classes for each piece to set moving rules
class King(Piece):
    def __init__(self, side: str):
        self.piece_type = "king"

        if (side.lower() != "dark") and (side.lower() != "light"):
            raise ValueError("Attribute 'side' must be 'dark' or 'light'")
        self.side = side
        self.is_dark = True if (self.side == "dark") else False
        self.is_light = not self.is_dark

        self.start_pos_row= 0 if self.is_dark else 7
        self.start_pos_col = 4 
        self.image_file_name = f"{self.piece_type}{1 if self.is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_pos_row
        self.current_pos_col = self.start_pos_col
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

        super().__init__(self.piece_type, 
                         side, 
                         self.is_dark,
                         self.is_light,
                         self.start_pos_row, 
                         self.start_pos_col, 
                         self.current_pos_row, 
                         self.current_pos_col, 
                         self.legal_moves, 
                         self.piece_range, 
                         self.image_file_name)


class Queen(Piece):
    def __init__(self, side: str):
        self.piece_type = "queen" 

        if (side.lower() != "dark") and (side.lower() != "light"):
            raise ValueError("Attribute 'side' must be 'dark' or 'light'")
        self.side = side
        self.is_dark = True if (self.side == "dark") else False
        self.is_light = not self.is_dark

        self.start_pos_row = 0 if self.is_dark else 7
        self.start_pos_col = 3 
        self.image_file_name = f"{self.piece_type}{1 if self.is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_pos_row
        self.current_pos_col = self.start_pos_col
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

        super().__init__(self.piece_type, 
                         side, 
                         self.is_dark,
                         self.is_light,
                         self.start_pos_row, 
                         self.start_pos_col, 
                         self.current_pos_row, 
                         self.current_pos_col, 
                         self.legal_moves, 
                         self.piece_range, 
                         self.image_file_name)

class Bishop(Piece):
    def __init__(self, side: str, count: int):
        self.piece_type = "bishop" 

        if (side.lower() != "dark") and (side.lower() != "light"):
            raise ValueError("Attribute 'side' must be 'dark' or 'light'")
        self.side = side
        self.is_dark = True if (self.side == "dark") else False
        self.is_light = not self.is_dark

        self.count = count ## 0 is the left piece, 1 is the right piece

        self.start_pos_row = 0 if self.is_dark else 7
        self.start_pos_col = 2 if (self.count == 0) else 5 
        self.image_file_name = f"{self.piece_type}{1 if self.is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_pos_row
        self.current_pos_col = self.start_pos_col
        self.legal_moves = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
        self.piece_range = 8 

        # x - 1, y + 1  top-left
        # x + 1, y + 1  top-right
        # x - 1, y - 1  bot-left
        # x + 1, y - 1  bot-right

        super().__init__(self.piece_type, 
                         side, 
                         self.is_dark,
                         self.is_light,
                         self.start_pos_row, 
                         self.start_pos_col, 
                         self.current_pos_row, 
                         self.current_pos_col, 
                         self.legal_moves, 
                         self.piece_range, 
                         self.image_file_name)

class Knight(Piece):
    def __init__(self, side: str, count: int):
        self.piece_type = "knight" 

        if (side.lower() != "dark") and (side.lower() != "light"):
            raise ValueError("Attribute 'side' must be 'dark' or 'light'")
        self.side = side
        self.is_dark = True if (self.side == "dark") else False
        self.is_light = not self.is_dark

        self.count = count ## 0 is the left piece, 1 is the right piece
        
        self.start_pos_row = 0 if self.is_dark else 7
        self.start_pos_col = 1 if (self.count == 0) else 6 
        self.image_file_name = f"{self.piece_type}{1 if self.is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_pos_row
        self.current_pos_col = self.start_pos_col
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

        super().__init__(self.piece_type, 
                         side, 
                         self.is_dark,
                         self.is_light,
                         self.start_pos_row, 
                         self.start_pos_col, 
                         self.current_pos_row, 
                         self.current_pos_col, 
                         self.legal_moves, 
                         self.piece_range, 
                         self.image_file_name)

class Rook(Piece):
    def __init__(self, side: str, count: int):
        self.piece_type = "rook" 

        if (side.lower() != "dark") and (side.lower() != "light"):
            raise ValueError("Attribute 'side' must be 'dark' or 'light'")
        self.side = side
        self.is_dark = True if (self.side == "dark") else False
        self.is_light = not self.is_dark

        self.count = count ## 0 is the left piece, 1 is the right piece

        self.start_pos_row = 0 if self.is_dark else 7
        self.start_pos_col = 0 if (self.count == 0) else 7
        self.image_file_name = f"{self.piece_type}{1 if self.is_dark else ""}.png"

        ## Legal moves
        self.current_pos_row = self.start_pos_row
        self.current_pos_col = self.start_pos_col
        self.legal_moves = [(0, 1), (-1, 0), (1, 0), (0, -1)]
        self.piece_range = 8

        # x + 0, y + 1  top
        # x - 1, y      left
        # x + 1, y      right
        # x + 0, y - 1  bot

        super().__init__(self.piece_type, 
                         side, 
                         self.is_dark,
                         self.is_light,
                         self.start_pos_row, 
                         self.start_pos_col, 
                         self.current_pos_row, 
                         self.current_pos_col, 
                         self.legal_moves, 
                         self.piece_range, 
                         self.image_file_name)

class Pawn(Piece):
    def __init__(self, side: str, count: int):
        self.piece_type = "pawn" 

        if (side.lower() != "dark") and (side.lower() != "light"):
            raise ValueError("Attribute 'side' must be 'dark' or 'light'")
        self.side = side
        self.is_dark = True if (self.side == "dark") else False
        self.is_light = not self.is_dark

        self.count = count ## 0 is the left piece, 1 is the right piece

        self.start_pos_row = 1 if self.is_dark else 6
        self.start_pos_col = self.count 
        self.image_file_name = f"{self.piece_type}{1 if self.is_dark else ""}.png"

        ## Legal moves
        ## En peassant enforced in board (get_legal_hints) to get context
        self.current_pos_row = self.start_pos_row
        self.current_pos_col = self.start_pos_col
        ## Pawns can only move forward, so black and white have different moves
        self.legal_moves = [(0, 1), (0, 2) if self.current_pos_row == self.start_pos_row else (0, 1)] + [(-1, 1), (1, 1)]
        # self.legal_moves = [(move[0], move[1] * -1) if is_dark else move for move in self.legal_moves]
        self.piece_range = 1
        
        super().__init__(self.piece_type, 
                         side, 
                         self.is_dark,
                         self.is_light,
                         self.start_pos_row, 
                         self.start_pos_col, 
                         self.current_pos_row, 
                         self.current_pos_col, 
                         self.legal_moves, 
                         self.piece_range, 
                         self.image_file_name)
