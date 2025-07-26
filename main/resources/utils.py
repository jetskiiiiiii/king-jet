from typing import List, Optional, Tuple

from resources.ui import *

# Left, top should already be to scale
def get_center_of_square(pos: Tuple):
    left, top = pos[0], pos[1]
    return left + (tile_size // 2), top + (tile_size // 2)

# To allow coordinates to be written on 8x8 grid and then here be converted to scale of actual board, based on tile size 
def scale_coor(coordinates: Tuple):
    return (tile_size * coordinates[0], tile_size * coordinates[1])

def get_square_that_was_clicked(mouse_pos: Tuple, return_unscaled_square_coor: bool = False):
    unscaled_square = (mouse_pos[0] // tile_size, mouse_pos [1] // tile_size)
    scaled_square = (unscaled_square[0] * tile_size, unscaled_square[1] * tile_size)
    if return_unscaled_square_coor:
        return scaled_square, unscaled_square 
    # Else just returned the scaled square
    return scaled_square
